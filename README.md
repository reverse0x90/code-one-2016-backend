# API Routes:

| Method | Route                              | Description                                                                            | Return                                    |
|--------|------------------------------------|----------------------------------------------------------------------------------------|-------------------------------------------|
| POST   | /login                             | Post a JSON with a username and password set: {'username': 'test', 'password': 'test'} | User Context JSON                         |
| GET    | /chores                            | Get a JSON of all available chores                                                     | JSON of all chore objects                 |
| GET    | /chores/[USERNAME]                 | Get a JSON of all chores assigned to [USERNAME]                                        | JSON of all chores assigned to [USERNAME] |
| POST   | /update/account/[USERNAME]/[VALUE] | Update the account balance for [USERNAME] to [VALUE]                                   | Update succeed or failed message          |
