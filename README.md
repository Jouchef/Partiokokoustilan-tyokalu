# Partiokokoustilan-tyokalu
Web app build from this project will be used by scout group Rastipartio to track the usage of their inventory (saws, tents, lanterns...). App will also be used to upkeep database about how many people use the space and when. This information is needed for Helsinki, and the amount of the yearly allowance city is paying to the Rastipartio is partly dictated by this information. ("24.1.2021, 1 man, 2 women, 10 boys, 9 girls")

In Finland, most scouts call their meeting place "kolo". In english it would be "burrow", tho probably this term is not used in english.


All the features listed:
1. Ability to register user to web app. 
  After registration Admin will need to certify account so the account is usable.
2. User can be moderator, or normal user
4. Normal user is able to add "kolo-activity" to "kolo-diary". This diary will be a form.
  4.1. For example: ("24.1.2021, 1 man, 2 women, 10 boys, 9 girls")
5. Administrator have the ability to accept user registering requests, because this system will be closed to specific people. (admin is able to delete users)
6. Administrator have the ability to make normal user administrator and administrator to normal user.
7. Admins are able to delete and add users.
8. Admins are able to update inventory lists.
  8.1. Item has name, description and amount of them.
9. Admins are able to print summary from "kolo-diary" for the use of the Rastipartio ry board.


These may be done later:
1. Normal user will be able to make a request for example that "There is no toilet paper" and this will be listed in a Requests-page.
  1.1. If someone fulfills this request, they are able to delete the request.
2. Normal user is able to lend items from inventory. (Not yet started)
  2.1. How long? What items? How many? who lends?
  2.2. User can easily search item by its name or description. (Not yet started)


-----------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------

# A BIT OF BACKGROUND

- I wasn't sure if this should be written in english or finnish, so I wrote this in english just in case.
- I have not yet done anything about the looks of the app, so sorry for that!
- I'm not sure if the Chrome warning about password breach is problem with my app????
- This is my very first html-project.
- At the moment, all the python-code is in one py-file. I will try to change that later when I have all the features done.
- I have created one new py-file. I gotta make app.py way smaller. 


# INSTRUCTIONS FOR TESTING - Read these well.

You are able to test the app in the following url: https://partiotyokalu.herokuapp.com/

Register normal user from the front page. After thet you will need to login to sadmin account to give the user a role. Otherwise your user-account wont be able to do anything.
To login to super admin account use the following credentials:
  un: sadmin@sadmin.sadmin
  pw: sadmin

You may also change normal users role to admin from "hallinnoi käyttäjiä" and see how that works.