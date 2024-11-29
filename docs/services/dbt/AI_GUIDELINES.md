# AI Guidelines for DBT Project Analysis

This document outlines the step-by-step process for AI to analyze and work with DBT projects effectively.

## 1. Project Structure Analysis

When encountering a DBT project:

1. First, identify the project root by looking for:
   - `dbt_project.yml` file
   - `models/` directory
   - `macros/` directory

2. Understand the model organization:
   - Check for standard directories: staging/, intermediate/, marts/
   - Note any custom directory structure
   - Look for patterns in file naming

## 2. Finding Model Files

When asked to find a specific model:

1. Start with exact match search:
   ```
   # Look for files matching the model name
   - models/**/{model_name}.sql
   - models/**/{model_name}.yml
   ```

2. If not found, try variations:
   - Check with and without prefixes/suffixes
   - Try both snake_case and kebab-case
   - Look for both .sql and .yml files

3. If multiple matches found:
   - Check model references in other files
   - Look for the most logical location based on model type
   - Consider the full path context

## 3. Analyzing Model Dependencies

To understand model relationships:

1. Parse SQL content:
   - Look for `ref('model_name')` calls
   - Check for `source('source_name', 'table_name')` calls
   - Identify CTEs and their dependencies

2. Follow dependency chain:
   - Start from the target model
   - Track both upstream (sources) and downstream (dependent models)
   - Note any circular references

3. Special cases to handle:
   - Jinja macros and their references
   - Variables and their usage
   - Custom functions and packages

## 4. Common Challenges and Solutions

### Multiple Models with Same Name

1. Resolution steps:
   - Check the full model path
   - Look at model references in other files
   - Consider the model's purpose and location
   - Use directory structure for context

### Case Sensitivity Issues

1. Search strategy:
   - First try exact case match
   - Then try case-insensitive match
   - Look for common patterns (all lowercase, snake_case)

### Complex Dependencies

1. Analysis approach:
   - Start with direct references
   - Look for macro usage
   - Check for variable substitutions
   - Consider config blocks

## 5. Best Practices for AI Analysis

1. **Always verify context**:
   - Check if we're in the correct project directory
   - Verify if we have access to all necessary files
   - Understand the project's naming conventions

2. **Handle errors gracefully**:
   - When a model isn't found, suggest similar names
   - If dependencies are unclear, list all possibilities
   - When encountering circular refs, explain the cycle

3. **Provide clear explanations**:
   - Explain why a particular file was chosen
   - Detail the dependency chain
   - Note any assumptions made

## 6. Practical Search Patterns

### For Model Files
```
# Primary search patterns
models/**/*.sql
models/**/*.yml

# Secondary patterns
models/**/[model_name].sql
models/**/[model_name].yml
```

### For References
```
# In SQL files
ref\(['"](.*?)['"]\)
source\(['"](.*?)['"],\s*['"](.*?)['"]\)

# In YAML files
models:
  - name:
```

## 7. Response Templates

### When Model is Found
```
I found the model '[model_name]' in [path].
Dependencies:
- Upstream: [list of models this depends on]
- Downstream: [list of models depending on this]
```

### When Model is Not Found
```
I couldn't find the exact model '[model_name]'. Here are possible alternatives:
1. [similar_name_1] in [path_1]
2. [similar_name_2] in [path_2]
Consider checking these locations or clarify if you're looking for a different model.
```

### When Analyzing Dependencies
```
The model '[model_name]' has the following dependency chain:
1. Direct dependencies:
   - [list of immediate refs]
2. Upstream sources:
   - [list of source tables]
3. Downstream impacts:
   - [list of dependent models]
```

## 8. Quality Checklist

Before providing answers, verify:
- [ ] Correct project context
- [ ] All relevant files checked
- [ ] Dependencies properly traced
- [ ] Naming conventions considered
- [ ] Potential ambiguities addressed
- [ ] Clear explanation prepared

## 9. Common Pitfalls to Avoid

1. Don't assume:
   - Standard directory structure
   - Consistent naming conventions
   - Single instance of model names

2. Always check:
   - Both SQL and YAML files
   - Macro references
   - Source definitions
   - Config blocks

3. Remember to:
   - Consider project-specific conventions
   - Look for documentation in YAML files
   - Check for disabled models
   - Verify schema references

## 10. Documentation Analysis

When documentation is needed:

1. Check these locations:
   ```
   models/[path]/schema.yml
   models/[path]/[model_name].yml
   ```

2. Look for:
   - Model descriptions
   - Column definitions
   - Tests
   - Tags and meta information

## Final Notes

- Always prioritize exact matches over partial matches
- Consider the full context of the project
- When in doubt, provide multiple options with explanations
- Document any assumptions made during analysis
