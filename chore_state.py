class Chore_Status_Stack:

  def __init__(self):
    self.stack = []
      
  def peek(self):
    return self.stack[-1]

  def push(self, username, title, status):
    self.stack.append({"username": username, "title": title, "status": status})

  def pop(self):
    return self.stack.pop()  