"""
# https://grok.com/share/bGVnYWN5_c01973e6-b130-4907-9e31-476eb1e349f4

The __post_init__ method in the EnterpriseContext dataclass is a dunder method that runs after the 
auto-generated __init__ to perform additional initialization.
It initializes security to a new SecurityContext instance and audit_trail to an empty list if their values are None.
This approach avoids issues with mutable defaults and allows complex objects to be initialized properly.
The method is critical for ensuring that each EnterpriseContext instance is correctly set up for use, especially in systems like the Agent framework where context objects are passed to various components.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional, List

class SecurityContext:
    def __init__(self):
        self.access_level = "default"

class TaskType(Enum):
    RESEARCH = "research"
    ANALYSIS = "analysis"

@dataclass
class EnterpriseContext:
    security: Optional[SecurityContext] = None
    task_type: TaskType = TaskType.RESEARCH
    audit_trail: Optional[List[str]] = None
    compliance_level: str = "standard"

    def __post_init__(self):
        if self.security is None:
            self.security = SecurityContext()
        if self.audit_trail is None:
            self.audit_trail = []
            
# Create an instance with default values
context = EnterpriseContext()

# Inspect the instance
print(context.security.access_level)  # Output: default
print(context.task_type)             # Output: TaskType.RESEARCH
print(context.audit_trail)           # Output: []
print(context.compliance_level)      # Output: standard

# Create a custom SecurityContext
custom_security = SecurityContext()
custom_security.access_level = "admin"

# Create an instance with some custom values
context = EnterpriseContext(
    security=custom_security,
    task_type=TaskType.ANALYSIS,
    audit_trail=["Log entry 1"],
    compliance_level="high"
)

# Inspect the instance
print(context.security.access_level)  # Output: admin
print(context.task_type)             # Output: TaskType.ANALYSIS
print(context.audit_trail)           # Output: ['Log entry 1']
print(context.compliance_level)      # Output: high


# BAD EXAMPLE
# from dataclasses import dataclass
# from typing import List


# @dataclass
# class BadExample:
#     audit_trail: List[str] = []  # Wrong: Mutable default

# # This will cause issues
# context1 = BadExample()
# context2 = BadExample()
# context1.audit_trail.append("Log 1")

# print(context1.audit_trail)  # Output: ['Log 1']
# print(context2.audit_trail)  # Output: ['Log 1']  # Shared list!
