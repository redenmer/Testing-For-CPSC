from flask import Flask, request, render_template

def edit_distance(word1, word2):
    m = len(word1)
    n = len(word2)
    
    # Create a distance matrix with (m+1) rows and (n+1) columns
    dp = [[0 for _ in range(n+1)] for _ in range(m+1)]
    
    # Initialize the first row and column
    for i in range(m+1):
        dp[i][0] = i
    for j in range(n+1):
        dp[0][j] = j
    
    # Fill the matrix
    for i in range(1, m+1):
        for j in range(1, n+1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j],    # Deletion
                                   dp[i][j-1],    # Insertion
                                   dp[i-1][j-1])  # Substitution
    
    # Backtrack to find the alignment
    alignment1 = []
    alignment2 = []
    i, j = m, n
    
    while i > 0 or j > 0:
        if i > 0 and j > 0 and word1[i-1] == word2[j-1]:
            alignment1.append(word1[i-1])
            alignment2.append(word2[j-1])
            i -= 1
            j -= 1
        else:
            if i > 0 and (j == 0 or dp[i][j] == dp[i-1][j] + 1):
                # Deletion
                alignment1.append(word1[i-1])
                alignment2.append('-')
                i -= 1
            elif j > 0 and (i == 0 or dp[i][j] == dp[i][j-1] + 1):
                # Insertion
                alignment1.append('_')
                alignment2.append(word2[j-1])
                j -= 1
            else:
                # Substitution
                alignment1.append(word1[i-1])
                alignment2.append(word2[j-1])
                i -= 1
                j -= 1
    
    # Reverse the alignments since we built them backwards
    alignment1.reverse()
    alignment2.reverse()
    
    return dp, ''.join(alignment1), ''.join(alignment2)

def print_matrix(matrix, word1, word2):
    m = len(word1)
    n = len(word2)
    
    # Print remaining rows
    for i in range(m+1):
        # Print row label
        for j in range(n+1):
            print(f"{matrix[i][j]:2}", end=" ")
        print()

def main():
    import sys
    
    # Hardcoded example words
    word1 = "Meeep"
    word2 = "Meeopo"
    
    matrix, align1, align2 = edit_distance(word1, word2)
    
    print("\n The Matrix:")
    print_matrix(matrix, word1, word2)
    
    print(f"\nEdit distance: {matrix[len(word1)][len(word2)]}")

    print("\nAlignment is: ")
    print(align1)
    print(align2)

if __name__ == "__main__":
    main()