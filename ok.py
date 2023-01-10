ff = 0

for i in range(180):
    filename = f'C://Users//User//Desktop//Fulcrum//My_paper//pythonProject//Pygame//ecs_tests//images//sprites//ak_47//animation//{i}.png'

    fname2 = f'C://Users//User//Desktop//Fulcrum//My_paper//pythonProject//Pygame//ecs_tests//images//sprites//ak_47//a//{ff}.png'

    if i % 2 == 0:
        with open(filename, mode='rb') as file:
            f = file.read()
            with open(fname2, mode='wb') as file2:
                file2.write(f)
        ff += 1