# API Routes:

| Method | Route              | Description                                                                                            | Return                                    |
|--------|--------------------|--------------------------------------------------------------------------------------------------------|-------------------------------------------|
| POST   | /login             | Post a JSON with a username and password set. Example: {'username': 'test', 'password': 'test'}        | User Context JSON                         |
| GET    | /chores            | Get a JSON of all available chores                                                                     | JSON of all chore objects                 |
| GET    | /chores/[USERNAME] | Get a JSON of all chores assigned to [USERNAME]                                                        | JSON of all chores assigned to [USERNAME] |
| POST   | /update/account/   | Post a JSON with a username and new account value set. . Example: {'username':'test', 'value':1337.50} | Update succeed or failed message          |
| POST   | /update/stage      | Post a JSON with a username and new stage value set. . Example: {'username':'test', 'stage':1}         | Update succeed or failed message          |
