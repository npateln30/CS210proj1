import operator
from statistics import mean

import numpy


def read_ratings_data(file):
    ratings = {}
    for line in open(file):
        (movie, rate, id) = line.split('|')
        if movie not in ratings:
            rating = [float(rate)]
            ratings[movie] = rating
        else:
            rating = float(rate)
            ratings[movie].append(rating)
    return ratings


def read_movie_genre(f):
    genres = {}
    for line in open(f):
        (genre, id, movie) = line.split('|')
        movies = movie.rstrip()
        genres[movies] = genre
    return genres


def create_genre_dict(dict):
    newDict = {}
    for key, val in dict.items():
        if val not in newDict:
            k = []
            newDict[val] = k
        k = (key)
        newDict[val].append(k)
    return newDict


def calculate_average_rating(dict):
    averages = {}
    for key, val in dict.items():
        avg = mean(val)
        limited_avg = round(avg, 2)
        averages[key] = limited_avg
    return averages


def get_popular_movies(average_movies, number=10):
    sort_tuples = sorted(average_movies.items(), key=lambda x: x[1], reverse=True)[:number]
    return dict(sort_tuples)


def filter_movies(average_movies, threshold=3):
    threshdict = {k: v for k, v in average_movies.items() if v >= threshold}
    return threshdict


def get_popular_in_genre(genre, gmoviesdict, avgmoviesdict, top=5):
    retrieveMovies = gmoviesdict.get(genre)
    moviewratings = [avgmoviesdict[x] for x in retrieveMovies]
    res = dict(zip(retrieveMovies, moviewratings))
    sort_tuples = sorted(res.items(), key=lambda x: x[1], reverse=True)[:top]
    return dict(sort_tuples)


def get_genre_rating(genre, gmoviesdict, avgmoviesdict):
    retrieveMovies = gmoviesdict.get(genre)
    moviewratings = [avgmoviesdict[x] for x in retrieveMovies]
    return round(mean(moviewratings),2)


def genre_popularity(genremovdict, movieavgdict, n=5):
    result_dict = dict()
    total = 0
    # for each value in each genre from dict1, iterate through corresponding key in 2.2
    for genre in genremovdict:
        total = 0
        for movie in genremovdict[genre]:
            # get each movies rating from dict22, and add to total, then divide by size to get the average
            total += movieavgdict[movie]
        average = total / len(genremovdict[genre])
        result_dict[genre] = round(average, 2)
        # at this point, the total has been computed and all of the movies part of the genre have been iterated through
        # get the size of the dict21[genre] and compute the average
    sort_tuples = sorted(result_dict.items(), key=lambda x: x[1], reverse=True)[:n]
    return dict(sort_tuples)


def read_user_ratings(file):
    users = {}
    for line in open(file):
        (movie, rate, id) = line.split('|')
        ids = int(id.rstrip())
        if ids not in users:
            rating = float(rate)
            users[ids] = [(movie, rating)]
        else:
            rating = float(rate)
            users[ids].append((movie, rating))
    return users

def get_user_genre(userId, userMovieDict, movieGenreDict):
    resultDict = dict()
    newDict = create_genre_dict(movieGenreDict)
    
    count = 0
    
    if userId in userMovieDict:
        for genre in newDict:
            total = 0
            for index, tuple in enumerate(userMovieDict[userId]):
                if tuple[0] in newDict[genre]:
                    count += 1
                    total += tuple[1]
                else:
                    continue
                average = total/count
                resultDict[genre] = round(average, 2)
    sortTuples = sorted(resultDict.items(), key = lambda x:x[1], reverse=True)
    res = list(dict(sortTuples).keys())[0]
    return res

def recommend_movies(userId, userMovieDict, movieGenreDict, movieAvgDict):
    #call function above to get favorite genre
    #use that genre to check the movies within movieGenreDict
    #check movies between userId and genre in Dictionary 
    #for the movies not in userMovieDict find the average ratings for them and store them in new dict
    #sort the new dict and return the top 3

    result = {}

    newDict = create_genre_dict(movieGenreDict)
    
    genre = get_user_genre(userId, userMovieDict, movieGenreDict)
    count = 0
    for key in newDict:
        if genre in newDict:
            total = 0
            for val, tuple in enumerate(userMovieDict[userId]):
                for x in newDict[genre]:
                    if tuple[0] != x:
                        count += 1
                        total += movieAvgDict[x]
                    else:
                        count = 0
                        total = 0
                        continue
                    average = total/count
                    result[x] = round(average,2)
        sortDict = sorted(result.items(), key = lambda x:x[1], reverse=True)[:3]
        if(len(sortDict) < 3):
            return result
        else:
            return sortDict




    

                   
                
def main():
    test = read_ratings_data("movieRatingSample.txt")
    print("1.1: ", test)
    test2 = read_movie_genre("genreMovieSample.txt")
    print("1.2: ", test2)
    test3 = create_genre_dict(test2)
    print("2.1: ", test3)
    test4 = calculate_average_rating(test)
    print("2.2: ", test4)
    test5 = get_popular_movies(test4, 1)
    print("3.1: ", test5)
    test6 = filter_movies(test4, 3)
    print("3.2: ", test6)
    test7 = get_popular_in_genre("Comedy", test3, test4, 2)
    print("3.3: ", test7)
    test8 = get_genre_rating("Adventure", test3, test4)
    print("3.4: ", test8)
    test9 = genre_popularity(test3, test4, 2)
    print("3.5: ", test9)
    test10 = read_user_ratings("movieRatingSample.txt")
    print("4.1: ", test10)
    test11 = get_user_genre(6, test10, test2)
    print("4.2: ", test11)
    test12 = recommend_movies(1, test10, test2, test4)
    print("4.3: ", test12)
    
    


if __name__ == "__main__":
    main()

# fileHandle = open(f, 'r')
#
# for line in fileHandle:
#     fields = line.split('|')
#
#     d = dict
#     print(fields[0])  # prints the first fields value
#     print(fields[1])  # prints the second fields value
#
# fileHandle.close()