
## Description

Please provide a clear and concise description of the issue.

### Issue Type

<!-- Please check the relevant option with "x" -->
- [ ] Bug Report
- [ ] Feature Request
- [ ] Documentation Improvement
- [ ] Question
- [ ] Other (Please specify)

## Steps to Reproduce

Provide a minimal code example or a detailed step-by-step description to reproduce the issue.

### System & Environment:

<!-- Provide information about your environment.
Most small bugs do not require all this information. -->
- **OS Platform**: (e.g., Linux Ubuntu 16.04)
- **Python version**: (e.g., Python 3.10)
- **`dvs_printf` version**: (e.g., dvs_printf 2.1)
- **Terminal/Console**: (e.g., Bash shell)

* *Add any additional configuration if needed.*

### Code

Provide code to help us reproduce your issue:
```
(You can paste code or attach files by dragging & dropping them below)
- Include code to invoke the errors and find the bugs. 
- Provide functions and parameters to reproduce the errors & bugs.
- Include code files & (video/photos) of the bugs.
```

1. **Imports**: functions you are using
    ```py
    from dvs_printf import init     # e.g.,

    pf = init(style="center")
    printf = pf.printf          # e.g., (printf)
    ```

2. **Given Values**: values that are given to the function 
    ```py
    values = [
        "this is a list of strings", 
        "given to the printf function",
        "to see the possible outcome"
    ]
    ```

3. **Parameters**: parameters that are given to the function
    ```py
    printf(
        values,             
        style="async", 
        speed=4, 
        delay=1,
        stay=False,
        getmat=True
    )
    ```

4. **Code or File:** 
    
    `drag & drop your files here -->`

## Expected Behavior

What should happen?

## Actual Behavior

What actually happens?

## Additional Information

Any additional information, configuration, or data that might be necessary to reproduce the issue.

### Possible Solution

If you have a possible solution or workaround, let us know

### Checklist

<!-- Check all the boxes with "x" to confirm -->
- [ ] I have read the [contributing guidelines](https://github.com/dhruvan-vyas/dvs_printf/blob/main/docs/CONTRIBUTING.md).
- [ ] I have searched the existing issues and this is not a duplicate.
- [ ] I have provided sufficient information above to help reproduce or understand the issue.

### Why This Is Important

- **Clarity and Reproducibility**: Providing clear steps ensures that others can reproduce the issue, which is critical for diagnosing and fixing bugs. Without this, maintainers might struggle to understand the problem or may not be able to reproduce it at all.
- **Efficiency**: Detailed steps help speed up the debugging process. Maintainers can quickly follow the provided steps without needing to spend time setting up or guessing the conditions that might trigger the bug.
- **Communication**: It ensures that the issue is communicated effectively, reducing back-and-forth communication to clarify details.

### Tips for Effective Bug Reporting

- **Be Specific**: Include specific details about the environment, such as the version of the module, Python version, and operating system.
- **Include Relevant Code**: Provide only the code necessary to reproduce the issue. Avoid including unrelated code that might obscure the problem.
- **Describe Expected vs. Actual Behavior**: Clearly state what you expected to happen and what actually happened, including any error messages or logs.

By following these guidelines, you help maintainers quickly understand and address the issue, making the process more efficient for everyone involved.

Thank you for reporting!
