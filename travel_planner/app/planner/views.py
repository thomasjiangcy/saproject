from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .utils import (
    tokenize_and_clean, get_topic_dist, filter_venues,
    sort_by_sentiment, retrieve_start_node,
    get_path, get_distance_dict
)

TIME_AT_EACH_VENUE = 1  # hour
SPEED_PER_KM = 40  # km/h


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

        # Pre-process words
        cleaned = tokenize_and_clean(preferences)

        # Infer topic distributions on user's preferences
        prefence_topic_dist = get_topic_dist(cleaned)

        # Filter venues based on venues based on document similarity of topics
        venues = filter_venues(prefence_topic_dist, hours)

        # Choose starting point from the list based on venue closest to 
        # the accommodation lat long
        starting_point = retrieve_start_node(venues, lat, lng)

        # Sort the filtered venues based on sentiment score
        sorted_venues = sort_by_sentiment(venues, starting_point)
        sorted_with_start = sort_by_sentiment(venues, starting_point, True)
        # Take the remaining venues and get the shortest route to connect all venues
        path = get_path(sorted_venues, starting_point)
        # Calculate the total time it would take to visit all venues
        # including the time spent at the venue and the time taken to travel between
        # each venue
        total_time = 0
        distance_dict = get_distance_dict(sorted_with_start, starting_point)
        for i, location in enumerate(path):
            total_time += 1
            if i != 0 and i != (len(path) - 1):
                prev_index = i - 1
                distance = distance_dict[location.id][path[prev_index].id]
                time_taken = distance / SPEED_PER_KM  # hours
                total_time += time_taken
        print('Total time: ', str(total_time))

        # Iteratively remove venues starting from the least popular until the total
        # time taken is lesser than or equal to the hours specified by the user
        while total_time > hours:
            sorted_venues = sorted_venues[:-1]  # remove the venue with least sentiment score
            sorted_with_start = sorted_venues + [starting_point]
            path = get_path(sorted_with_start, starting_point)
            total_time = 0
            distance_dict = get_distance_dict(sorted_with_start, starting_point)
            for i, location in enumerate(path):
                total_time += 1
                if i != 0 and i != (len(path) - 1):
                    prev_index = i - 1
                    curr = location.id
                    prev = path[prev_index].id
                    distance = distance_dict[curr][prev]
                    time_taken = distance / SPEED_PER_KM  # hours
                    total_time += time_taken
            print('Total time: ', str(total_time))

        parsed_path = []
        for location in path:
            obj = {
                'id': location.id,
                'name': location.name,
                'lat': location.lat,
                'lng': location.long
            }
            parsed_path.append(obj)

        # Return the response in the form of a list of venues sorted according
        # to the order in which they should be visited

        return Response({'data': parsed_path}, status=status.HTTP_200_OK)