"""
    listrotate.py
"""

def main():
    hearts = [" :purple_heart: ", " :yellow_heart: ", " :blue_heart: ", " :green_heart: ", " :heart: "]

    for i in range(0, 25):
        hearts.append(hearts.pop(0))
        print(f'{i}: {"".join(hearts)}')

    return True

if __name__ == '__main__':
    main()
