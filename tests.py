from functions.get_files_info import get_files_info

test1 = get_files_info("calculator", ".")
test2 = get_files_info("calculator", "pkg")
test3 = get_files_info("calculator", "/bin")
test4 = get_files_info("calculator", "../")
print("Result for current directory:")
print(test1)
print("Result for 'pkg' directory:")
print(test2)
print("Result for '/bin' directory:")
print(f"    {test3}")
print("Result for '../' directory:")
print(f"    {test4}")