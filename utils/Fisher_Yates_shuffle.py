import random
"""
- Implementation of Fisher_Yates shuffle algorithm. 
- The probability of each element is 1/n. 
- The assumption here is given a random function running in O(1) time. 
- Runtime: O(N) 
- Space: O(1)
"""
def Fisher_Yates_randomize(songs):
    if not songs:
        return []
    for i in range(len(songs)-1, 0, -1):
        #pick a random number from 0 to i
        j = random.randint(0, i)
        #swap arr[i] and arr[j]
        
        songs[i], songs[j] = songs[j], songs[i]
    return songs


if __name__ == "__main__":
    songs = [1, 2, 3, 4, 5]
    print(Fisher_Yates_randomize(songs))
    