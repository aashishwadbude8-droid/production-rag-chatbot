def remember_variable(session_state, variable_info):
    """
    Store the last variable in session state.
    """

    session_state["last_variable"] = variable_info


def get_last_variable(session_state):
    """
    Return last remembered variable.
    """

    return session_state.get("last_variable", None)


def clear_memory(session_state):
    """
    Reset conversation memory.
    """

    if "last_variable" in session_state:
        del session_state["last_variable"]