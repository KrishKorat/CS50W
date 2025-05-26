def announce(f):
  def wrapper():
    print("About to run the function")
    f()
    print("Done with the function")
  return wrapper


@announce
def hello():
  print("Hello, world")


hello()

'''
About to run the function
Hello, world
Done with the function
'''