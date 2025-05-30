# Advanced Pydantic Integration Example
# https://openai.github.io/openai-agents-python/tools/

import asyncio
from typing import List, Optional, Literal, Union
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, model_validator
from agents import Agent, Runner, function_tool, FunctionTool

# =============================================================================
# ADVANCED PYDANTIC MODELS FOR TOOL PARAMETERS AND RETURNS
# =============================================================================


class Priority(str, Enum):
    """Task priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TaskStatus(str, Enum):
    """Task status options"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Task(BaseModel):
    """A task with full validation and constraints"""
    id: int = Field(..., description="Unique task identifier", ge=1)
    title: str = Field(..., description="Task title",
                       min_length=1, max_length=100)
    description: Optional[str] = Field(
        None, description="Detailed description", max_length=500)
    priority: Priority = Field(
        default=Priority.MEDIUM, description="Task priority level")
    status: TaskStatus = Field(
        default=TaskStatus.PENDING, description="Current task status")
    due_date: Optional[datetime] = Field(None, description="Task due date")
    tags: List[str] = Field(default_factory=list,
                            description="Task tags", max_length=10)
    estimated_hours: Optional[float] = Field(
        None, description="Estimated hours", ge=0.1, le=1000)

    @field_validator('tags')
    @classmethod
    def validate_tags(cls, v):
        """Validate that tags are unique and not empty"""
        if len(v) != len(set(v)):
            raise ValueError("Tags must be unique")
        for tag in v:
            if not tag.strip():
                raise ValueError("Tags cannot be empty")
        return v

    @model_validator(mode='after')
    def validate_task(self):
        """Cross-field validation"""
        # High priority tasks should have due dates
        if self.priority == Priority.URGENT and not self.due_date:
            raise ValueError("Urgent tasks must have a due date")
        return self


class TaskFilter(BaseModel):
    """Filtering criteria for tasks"""
    status: Optional[TaskStatus] = Field(None, description="Filter by status")
    priority: Optional[Priority] = Field(
        None, description="Filter by priority")
    tag: Optional[str] = Field(None, description="Filter by tag")
    limit: int = Field(default=10, description="Maximum results", ge=1, le=100)


class TaskSearchResult(BaseModel):
    """Search results with metadata"""
    tasks: List[Task] = Field(..., description="List of matching tasks")
    total_count: int = Field(..., description="Total number of matching tasks")
    filtered_count: int = Field(...,
                                description="Number of results after filtering")
    has_more: bool = Field(..., description="Whether there are more results")


class TaskOperationResult(BaseModel):
    """Result of task operations"""
    success: bool = Field(..., description="Whether operation succeeded")
    message: str = Field(..., description="Operation result message")
    task_id: Optional[int] = Field(None, description="ID of affected task")
    errors: List[str] = Field(default_factory=list,
                              description="Any validation errors")

# =============================================================================
# FUNCTION TOOLS WITH ADVANCED PYDANTIC INTEGRATION
# =============================================================================


# In-memory task storage for demo
TASKS_DB: List[Task] = [
    Task(id=1, title="Setup development environment", priority=Priority.HIGH,
         description="Setup dev environment", due_date=None,
         tags=["development", "setup"], estimated_hours=4.0),
    Task(id=2, title="Write unit tests", priority=Priority.MEDIUM,
         description="Write comprehensive tests", due_date=None,
         tags=["testing", "development"], estimated_hours=8.0),
    Task(id=3, title="Deploy to production", priority=Priority.URGENT,
         description="Deploy application",
         tags=["deployment", "production"], estimated_hours=2.0,
         due_date=datetime(2024, 12, 31))
]


@function_tool
def create_task(task_data: Task) -> TaskOperationResult:
    """Create a new task with full validation.

    Args:
        task_data: Complete task information with validation
    """
    try:
        # Check if task ID already exists
        if any(task.id == task_data.id for task in TASKS_DB):
            return TaskOperationResult(
                success=False,
                message=f"Task with ID {task_data.id} already exists",
                task_id=None,
                errors=["Duplicate task ID"]
            )

        # Add to database
        TASKS_DB.append(task_data)

        return TaskOperationResult(
            success=True,
            message=f"Task '{task_data.title}' created successfully",
            task_id=task_data.id
        )
    except Exception as e:
        return TaskOperationResult(
            success=False,
            message="Failed to create task",
            task_id=None,
            errors=[str(e)]
        )


@function_tool
def search_tasks(filters: TaskFilter) -> TaskSearchResult:
    """Search for tasks with advanced filtering.

    Args:
        filters: Search and filter criteria
    """
    # Apply filters
    filtered_tasks = TASKS_DB.copy()

    if filters.status:
        filtered_tasks = [
            t for t in filtered_tasks if t.status == filters.status]

    if filters.priority:
        filtered_tasks = [
            t for t in filtered_tasks if t.priority == filters.priority]

    if filters.tag:
        filtered_tasks = [t for t in filtered_tasks if filters.tag in t.tags]

    total_count = len(filtered_tasks)

    # Apply limit
    limited_tasks = filtered_tasks[:filters.limit]
    has_more = len(filtered_tasks) > filters.limit

    return TaskSearchResult(
        tasks=limited_tasks,
        total_count=len(TASKS_DB),
        filtered_count=total_count,
        has_more=has_more
    )


@function_tool
def update_task_status(task_id: int, new_status: TaskStatus) -> TaskOperationResult:
    """Update a task's status with validation.

    Args:
        task_id: ID of task to update
        new_status: New status value
    """
    try:
        # Find task
        task = next((t for t in TASKS_DB if t.id == task_id), None)
        if not task:
            return TaskOperationResult(
                success=False,
                message=f"Task with ID {task_id} not found",
                task_id=None,
                errors=["Task not found"]
            )

        # Validate status transition
        if task.status == TaskStatus.COMPLETED and new_status != TaskStatus.COMPLETED:
            return TaskOperationResult(
                success=False,
                message="Cannot change status of completed task",
                task_id=None,
                errors=["Invalid status transition"]
            )

        old_status = task.status
        task.status = new_status

        return TaskOperationResult(
            success=True,
            message=f"Task status updated from {old_status} to {new_status}",
            task_id=task_id
        )
    except Exception as e:
        return TaskOperationResult(
            success=False,
            message="Failed to update task status",
            task_id=None,
            errors=[str(e)]
        )

# =============================================================================
# MANUAL FUNCTION TOOL WITH STRICT SCHEMA
# =============================================================================


class ComplexCalculationInput(BaseModel):
    """Complex calculation input with strict validation"""
    operation: Literal["add", "multiply", "power", "factorial"] = Field(
        ..., description="Mathematical operation to perform"
    )
    numbers: List[float] = Field(
        ..., description="Numbers to operate on", min_length=1, max_length=10
    )
    precision: int = Field(
        default=2, description="Decimal places for result", ge=0, le=10
    )

    @field_validator('numbers')
    @classmethod
    def validate_numbers(cls, v, info):
        """Validate numbers based on operation"""
        operation = info.data.get('operation') if info.data else None

        if operation == "factorial":
            if len(v) != 1:
                raise ValueError("Factorial requires exactly one number")
            if v[0] < 0 or v[0] != int(v[0]):
                raise ValueError("Factorial requires non-negative integer")

        if operation == "power":
            if len(v) != 2:
                raise ValueError(
                    "Power operation requires exactly two numbers")

        return v


class CalculationResult(BaseModel):
    """Calculation result with metadata"""
    result: float = Field(..., description="Calculation result")
    operation: str = Field(..., description="Operation performed")
    input_numbers: List[float] = Field(..., description="Input numbers")
    computation_time: float = Field(..., description="Time taken in seconds")


async def complex_calculation(ctx, args: str) -> str:
    """Perform complex mathematical calculations with strict validation"""
    import time
    import math

    start_time = time.time()

    try:
        # Parse and validate input
        input_data = ComplexCalculationInput.model_validate_json(args)

        # Perform calculation
        numbers = input_data.numbers
        operation = input_data.operation

        if operation == "add":
            result = sum(numbers)
        elif operation == "multiply":
            result = 1
            for num in numbers:
                result *= num
        elif operation == "power":
            result = numbers[0] ** numbers[1]
        elif operation == "factorial":
            result = math.factorial(int(numbers[0]))
        else:
            raise ValueError(f"Unknown operation: {operation}")

        # Round to specified precision
        result = round(result, input_data.precision)

        computation_time = time.time() - start_time

        # Create result object
        calc_result = CalculationResult(
            result=result,
            operation=operation,
            input_numbers=numbers,
            computation_time=computation_time
        )

        return calc_result.model_dump_json(indent=2)

    except Exception as e:
        return f"Calculation error: {str(e)}"

# Manual FunctionTool creation with strict schema


def get_strict_json_schema():
    """Get a strict JSON schema for complex calculation."""
    schema = ComplexCalculationInput.model_json_schema()

    # Ensure strict mode compatibility
    def make_strict(obj):
        if isinstance(obj, dict):
            if "properties" in obj:
                obj["additionalProperties"] = False
                # For strict mode, all properties must be required
                if "required" not in obj:
                    obj["required"] = []
                obj["required"] = list(obj["properties"].keys())
            for value in obj.values():
                make_strict(value)
        elif isinstance(obj, list):
            for item in obj:
                make_strict(item)

    make_strict(schema)
    return schema


complex_calc_tool = FunctionTool(
    name="complex_calculation",
    description="Perform complex mathematical calculations with strict validation",
    params_json_schema=get_strict_json_schema(),
    on_invoke_tool=complex_calculation,
    strict_json_schema=True  # Enable strict mode for better validation
)

# =============================================================================
# MAIN DEMO
# =============================================================================


async def main():
    print("OpenAI Agents SDK - Advanced Pydantic Integration")
    print("=" * 60)

    # Create agent with advanced Pydantic tools
    agent = Agent(
        name="Task Management Assistant",
        instructions="""You are a task management assistant with access to advanced tools:
        1. create_task - Create new tasks with full validation
        2. search_tasks - Search and filter tasks
        3. update_task_status - Update task status
        4. complex_calculation - Perform mathematical calculations
        
        Always validate inputs and provide detailed feedback about any errors.
        Use the structured responses to provide helpful information.""",
        tools=[create_task, search_tasks,
               update_task_status, complex_calc_tool]
    )

    # Test 1: Create a valid task
    print("=== Test 1: Create Valid Task ===")
    result1 = await Runner.run(
        agent,
        input="""Create a new task:
        - ID: 4
        - Title: "Implement user authentication"
        - Priority: high
        - Tags: ["security", "backend"]
        - Estimated hours: 12.5"""
    )
    print(f"Result: {result1.final_output}\n")

    # Test 2: Try to create an invalid task (should show validation errors)
    print("=== Test 2: Create Invalid Task (Missing Due Date for Urgent) ===")
    result2 = await Runner.run(
        agent,
        input="""Create a new task:
        - ID: 5
        - Title: "Fix critical bug"
        - Priority: urgent
        - No due date specified"""
    )
    print(f"Result: {result2.final_output}\n")

    # Test 3: Search tasks with filters
    print("=== Test 3: Search Tasks ===")
    result3 = await Runner.run(
        agent,
        input="Search for all high priority tasks, limit to 5 results"
    )
    print(f"Result: {result3.final_output}\n")

    # Test 4: Complex calculation
    print("=== Test 4: Complex Calculation ===")
    result4 = await Runner.run(
        agent,
        input="Calculate the factorial of 5 with 3 decimal places precision"
    )
    print(f"Result: {result4.final_output}\n")

    # Test 5: Invalid calculation (should show validation errors)
    print("=== Test 5: Invalid Calculation ===")
    result5 = await Runner.run(
        agent,
        input="Calculate the factorial of -3"
    )
    print(f"Result: {result5.final_output}")

if __name__ == "__main__":
    asyncio.run(main())
