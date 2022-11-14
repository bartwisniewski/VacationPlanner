# 1. Application core flow

Date: 2022.11.05

## Status

Proposed

## Context

Core of the application is to create vacation events for a group of friends and match them with the best date and place. The event will develop in a sequencial way to follow user decisions

## Decision

Application flow:
1. Register and login
2. Configure your family (adults, children, infants)
3. Create or join a group
4. Create event for a group and automatically add all group members to it
5. At each step members of a group can leave the event
6. Each group member can propose and vote on a date (start and end of the event). After voting each member of a group must confirm finishing this step.
7. Date is approved by a event master / admin
8. Users can propose and vote on a place to go by giving the link to the place found in the internet and fullfilling all necessary information for other members. After voting each member of a group must confirm finishing this step.
9. Place is approved by a event master / admin
10. User that proposed selected place gets an email and internal notification to book this place
11. User that proposed selected place mark it as booked or retrieve the proposal to go back to place selection. He can also give information about advance payment etc.
12. Event is marked as fixed and application can create event on external social media services like facebook
