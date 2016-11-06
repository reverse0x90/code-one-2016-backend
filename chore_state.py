class Chore_Status_Stack:

  def __init__(self):
    self.stack = []
      
  def push(self, username, title, status):
    self.stack.append({"username": username, "title": title, "status": status})
  def pop(self):
    return self.stack.pop()  