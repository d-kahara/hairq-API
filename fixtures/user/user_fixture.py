user_mutation_query = '''
mutation {
  createUser(
      name:"testUser1", email:"test1@hairq.co.uk", passwordHash:"Pass@123") {
    user {
      email
      name
      state
    }
  }
}

'''

user_mutation_response = {
  "data": {
    "createUser": {
      "user": {
        "email": "test1@hairq.co.uk",
        "name": "testUser1",
        "state": "ACTIVE"
      }
    }
  }
}
