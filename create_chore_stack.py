import cPickle as pickle
from chore_state import Chore_Status_Stack

status_stack = Chore_Status_Stack()

with open('chore_state.p', 'wb') as pickle_file:
	pickle.dump(status_stack, pickle_file)