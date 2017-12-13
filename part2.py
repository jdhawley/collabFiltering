input_filename = "input.txt"
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


def get_predicted_score_memory(row_number, col_number, ratings, average_ratings, weights):
    """
    Predicts a rating for a row, column combination.

    This corresponds to the "Recommendation Score" on Jonathan's solution sheet.
    """
    top = calculate_top_half_recommendation(row_number, col_number, ratings, average_ratings, weights)
    return round(average_ratings[row_number] + (top / sum(list(map(abs, weights[row_number])))), 1)

def calculate_model_numerator(query_user, query_index, ratings, items, weights):
	"""
	Calculates and returns the sum of (sim(i,N)*R(u,N))
	"""
	near, tmp = ([] for i in range(2))
	for user in ratings:
		near.append(user[query_index])
	for idx in items:
		far = []
		for user in ratings:
			far.append(user[idx])
		tmp.append(get_sim(near,far,weights, query_user) * user[idx])
	print("Numerator: ", tmp)
	return sum(tmp)

def calculate_model_denominator(query_user, query_index, ratings, items, weights):
	"""
	Calculates and returns the sum of (abs(sim(i,N))) where i is the item and N 
	is the set of items 
	"""
	near, tmp = ([] for i in range(2))
	for user in ratings:
		near.append(user[query_index])
	for idx in items:
		far = []
		for user in ratings:
			far.append(user[idx])
		tmp.append(abs(get_sim(near, far, weights, query_user)))
	print("denominator: ", tmp)
	return sum(tmp)

def get_sim(near, far, averages, user_idx):
	""" 
	Near is the item that is being queried. Far is a similar item.
	Returns the adjusted cosine similarity between near and far.
	"""

	print()
	
	num, runningNear, runningFar, denom = ([] for i in range(4))
	for n in range(len(near)-1):
		c = near[n] - averages[n]
		d = far[n] - averages[n]
		num.append(c*d)
		print("c: ", c)
		print("d: ", d)
		runningNear.append(c ** 2)
		runningFar.append(d ** 2)

	numerator = sum(num)
	denom = (sum(runningNear) ** .5) * (sum(runningFar) ** .5)
	print("sim_num: ", numerator)
	print("sim_den: ", denom)
	print("num/den: ", numerator/denom)
	if(denom == 0):
		print("Divide by 0")
		return 0
	
	return numerator / denom

def get_predicted_score_model(user_num, item_num, ratings, weights):
	"""
	Predicts a rating for an item for a specific user using a model-
	based approach. This is assignment 2.
	
	Implements a weighted sum.
	"""
	items = get_relevant_items(ratings[user_num], ratings)
	top = calculate_model_numerator(user_num, item_num, ratings, items, weights)
	bottom = calculate_model_denominator(user_num, item_num, ratings, items, weights)
	if (bottom == 0):
		print("Divide by 0!")
		return 0
	return top / bottom

def get_relevant_items(user, ratings):
	"""
	Return each item (col) for which queryUser has a rating 
	"""
	ls = []
	for idx in range(0,len(user)):
		if(user[idx] != 0):
			ls.append(idx)
	return ls
	
'''
def calculate_model_numerator(user):
	Find list of all users who have ranked both items. Get all similarItems from that list.
	Get the similarity value between queryItem and each similarItem. Multiply each similarity value
	by the queryUser's ranking for similarItem. Sum the resulting list.
	return sum()

def calculate_model_denominator():
	Find list of all users who have ranked both items. Get all similarItems from that list.
	Get the similarity value between queryItem and each similarItem. Take the absolute value of each
	similarity value, then return the sum of the list
	sim_items = []
	sim_vals = []
	for sim_item in sim_items:
		sim_vals.append(abs(sim(sim_item, query_item)))
	return sum(sim_vals)
'''

def listSims():
	return 

def main():
	print("Crunching numbers, please wait...\n")
	ratings = get_user_ratings(input_filename)
	average_ratings = get_averages(ratings)
	weights = get_all_weights(test_row, ratings, average_ratings)

	choice = int(input("Choose part 1 or 2: "))	
	if(choice == 1):
		while True:
			row_number = int(input("Please enter the user (row) to predict: "))
			col_number = int(input("Please enter the item (column) to predict: "))
			predicted_score = get_predicted_score_memory(row_number, col_number, ratings, average_ratings, weights)
			print("The predicted score is: " + str(predicted_score) + "\n")
	else:
		while True: 
			row_number = int(input("Please enter the user (row) to predict: "))
			col_number = int(input("Please enter the item (column) to predict: "))
			predicted_score = get_predicted_score_model(row_number, col_number, ratings, average_ratings) + average_ratings[row_number]
			print("The predicted score is: " + str(put_in_bucket(predicted_score)) + "\n")

def put_in_bucket(flt):
	if (flt > 5):
		return 5
	return int(flt)	

if __name__ == "__main__":
    main()
