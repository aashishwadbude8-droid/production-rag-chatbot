import re


def infer_datatype(value):
    """
    Infer Python datatype from extracted value.
    """

    value = value.strip()

    if (
        value.startswith('"') and value.endswith('"')
    ) or (
        value.startswith("'") and value.endswith("'")
    ):
        return "str"

    if re.fullmatch(r"-?\d+", value):
        return "int"

    if re.fullmatch(r"-?\d+\.\d+", value):
        return "float"

    if value in ["True", "False"]:
        return "bool"

    if value.startswith("[") and value.endswith("]"):
        return "list"

    if value.startswith("(") and value.endswith(")"):
        return "tuple"

    if value.startswith("{") and value.endswith("}"):
        return "dict"

    return "unknown"


def extract_variables(documents):
    """
    Extract Python variable assignments from all documents.
    """

    variables = {}

    pattern = re.compile(
        r"([a-zA-Z_]\w*)\s*=\s*(\".*?\"|\'.*?\'|\[.*?\]|\{.*?\}|\(.*?\)|[^\s]+)"
    )

    for doc in documents:

        matches = pattern.findall(doc.page_content)

        for var, value in matches:

            variables[var] = {
                "value": value,
                "datatype": infer_datatype(value),
                "page": doc.metadata.get("page"),
                "file": doc.metadata.get("filename")
            }

    return variables


def get_variable(variable_name, variables):
    """
    Return single variable information.
    """

    return variables.get(variable_name)