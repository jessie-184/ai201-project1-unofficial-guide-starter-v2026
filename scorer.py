def judge(question, expects, answer, results) -> bool:
    """
    Judge the answer based on the question, expected answers, and results.

    Args:
        question (str): The question being asked.
        expects (str): The expected answer.
        answer (str): The answer provided.
        results (dict): A dictionary containing additional results or context.

    Returns:
        bool: True if the expected answer is found in the provided answer, False otherwise.
    """
    # Implement the logic to judge the answer here
    return expects.lower().strip() in answer.lower()