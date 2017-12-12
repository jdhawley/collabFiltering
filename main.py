input_filename = "testinput.txt"
test_row = 2


def get_user_ratings(fn):
    """
    Reads in the values and returns them as a list of lists.
    """
    fp = open(input_filename, "r")
    ratings = []
    for line in fp:
        ratings.append(list(map(int, line.split())))
    return ratings


def get_averages(ratings):
    """
    Returns a list of the average rating for each user.
    """
    average_ratings = []
    sum_ratings = 0
    num_ratings = 0
    for row in ratings:
        for rating in row:
            if rating != 0:
                sum_ratings += rating
                num_ratings += 1
        average_ratings.append(sum_ratings / num_ratings)
        sum_ratings = 0
        num_ratings = 0
    return average_ratings


def calculate_top_half_vector_similarity(row_one, row_two, ratings, average_ratings):
    """
    Calculates the top half of the vector similarity equation for two rows.

    This corresponds to "X" on Jonathan's solution sheet.
    """
    sum_ratings_minus_averages = 0
    for col_number in range(len(ratings[row_one])):
        if ratings[row_one][col_number] != 0 and ratings[row_two][col_number] != 0:
            first_difference = ratings[row_one][col_number] - average_ratings[row_one]
            second_difference = ratings[row_two][col_number] - average_ratings[row_two]
            sum_ratings_minus_averages += first_difference * second_difference

    return sum_ratings_minus_averages


def calculate_bottom_half_vector_similarity(row_one, row_two, ratings, average_ratings):
    """
    Calculates the bottom half of the vector similarity equation for two rows.

    This corresponds to "(Y * Z)" on Jonathan's solution sheet.
    """
    row_one_sum = 0
    row_two_sum = 0
    for col_number in range(len(ratings[row_one])):
        if ratings[row_one][col_number] != 0 and ratings[row_two][col_number] != 0:
            row_one_sum += (ratings[row_one][col_number] - average_ratings[row_one]) ** 2
            row_two_sum += (ratings[row_two][col_number] - average_ratings[row_two]) ** 2

    return (row_one_sum ** .5) * (row_two_sum ** .5)


def calculate_vector_similarity_weight(row_one, row_two, ratings, average_ratings):
    """
    Calculates the weight between two rows/users.

    This corresponds to the "Vector Similarity" score on Jonathan's solution sheet.
    """
    top = calculate_top_half_vector_similarity(row_one, row_two, ratings, average_ratings)
    bottom = calculate_bottom_half_vector_similarity(row_one, row_two, ratings, average_ratings)

    if top == 0 or bottom == 0:
        return 0

    return top / bottom


def get_all_weights(test_row, ratings, average_ratings):
    """
    Returns the weight of every row when compared to the passed in row.
    """
    weights = []
    for i in range(len(ratings)):
        weights.append([])
        for j in range(len(ratings)):
            if i == j:
                weights[i].append(0)
            else:
                weights[i].append(calculate_vector_similarity_weight(i, j, ratings, average_ratings))

    return weights


def calculate_top_half_recommendation(test_row, col_number, ratings, average_ratings, weights):
    """
    Calculates the top half of the recommendation equation.

    This corresponds to "N" on Jonathan's solution sheet.
    """
    total = 0
    for row_number in range(len(ratings)):
        if ratings[row_number][col_number] != 0:
            total += weights[row_number][test_row] * (ratings[row_number][col_number] - average_ratings[row_number])

    return total


def get_predicted_score(row_number, col_number, ratings, average_ratings, weights):
    """
    Predicts a rating for a row, column combination.

    This corresponds to the "Recommendation Score" on Jonathan's solution sheet.
    """
    top = calculate_top_half_recommendation(row_number, col_number, ratings, average_ratings, weights)
    return round(average_ratings[row_number] + (top / sum(list(map(abs, weights[row_number])))), 1)


def main():
    print("Crunching numbers, please wait...\n")
    ratings = get_user_ratings(input_filename)
    average_ratings = get_averages(ratings)
    weights = get_all_weights(test_row, ratings, average_ratings)

    while True:
        row_number = int(input("Please enter the user (row) to predict: "))
        col_number = int(input("Please enter the item (column) to predict: "))
        predicted_score = get_predicted_score(row_number, col_number, ratings, average_ratings, weights)
        print("The predicted score is: " + str(predicted_score) + "\n")


if __name__ == "__main__":
    main()
