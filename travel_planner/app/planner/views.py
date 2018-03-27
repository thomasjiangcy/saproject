from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class PlanView(APIView):
    """
    Main interface for Travel Planner
    """

    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        hours = int(request.data['hours'])
        lat = request.data['accommodation']['lat']
        lng = request.data['accommodation']['lng']
        preferences = request.data['preferences']
        mode = request.data.get('mode', 'lda')

        print(hours)
        print(lat)
        print(lng)
        print(preferences)
        print(mode)

        # Pre-process words to get BOW

        # Infer topic distributions on user's preferences

        # Filter venues based on venues based on document similarity of topics

        # Sort the filtered venues based on sentiment score

        # Choose starting point from the list based on venue closest to 
        # the accommodation lat long

        # Take the remaining venues and get the shortest route to connect all venues

        # Calculate the total time it would take to visit all venues
        # including the time spent at the venue and the time taken to travel between
        # each venue

        # Iteratively remove venues starting from the least popular until the total
        # time taken is lesser than or equal to the hours specified by the user

        # Return the response in the form of a list of venues sorted according
        # to the order in which they should be visited

        from time import sleep
        sleep(2)

        return Response({'message': 'Data loaded'}, status=status.HTTP_200_OK)