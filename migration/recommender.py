def recommend(analysis):
    recommendations = []

    if analysis["complex_functions"]:
        recommendations.append("Refactor large functions into smaller units")

    if analysis["issues"]:
        recommendations.append("Replace unsafe legacy APIs")

    recommendations.append("Add type hints and dataclasses")
    recommendations.append("Use repository/service pattern")

    return recommendations
