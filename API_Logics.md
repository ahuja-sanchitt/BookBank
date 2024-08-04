
# API Logics

## Overview
This is a bookbank app with features like searching books, adding recommendations, etc. Some endpoints like register, login, and search books are public since anyone should be able to access these. Other endpoints such as adding/viewing/filtering recommendations, liking, and commenting are authorized endpoints that require user registration to access.
All the data is managed in a local database, including recommendations, likes, and comments.
SwaggerUI documentation is available at `/swagger/`.
UUid is used everywhere

## API Types
There are two separate kinds of APIs for this project:
1. **Integrated with Frontend**: These APIs have features like login, register, view recommendations, etc.
2. **Standalone Endpoints**: These APIs are created solely for endpoint purposes and can be later integrated with frontend libraries like React.js.

## Endpoints

### Public Endpoints

#### `/loginuser/`
- This endpoint takes username and password, and then validates it with the database, if the details are correct then the user is logged in and jwt tokens are provided so the user can access the authorized endpoints

#### `/registeruser/`
- This endpoint takes username,email,password and registers the user. The password is encrypted when storing in the database.

### Authorized Endpoints

#### `/get_recommendations/`
- This endpoint needs jwt token to be passed, if the token is correct, random 10 recommendations are displayed, otherwise unauthorized error is shown.


#### `/submit_recommendations/`
- This endpoint takes bookname,recommendationtext,rating, userid and jwt token. Assuming that userid,jwt token is passed from the frontend for the current active user.if all the params are correct then recommendation is stored

#### `/like/`
- This endpoint takes the recommendationID(which recommendation is to be liked) and jwt token. RecommendationID is to be passed from the frontend. In the DB, like_count is increased for that recommendation on successfull execution of this endpoint

#### `/comment/`
- This endpoint takes userid,recommendationid,comment text,jwttoken. UserID and RecommendationID is to be passed from the frontend, to store details such as which user commented on which recommendation.

#### `/filter/`
- This endpoint takes params like rating,publication_date,sort_by. You can filter the recommendations based on rating or publication_date, and also sort them based on the same options.

#### `/token/`
-This endpoint is just for internal use to check/get jwt tokens for a user
