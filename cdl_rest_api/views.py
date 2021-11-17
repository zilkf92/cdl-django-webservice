from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response  # Standard Response object
from rest_framework import status
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from cdl_rest_api import serializers
from cdl_rest_api import models
from cdl_rest_api import permissions

# instead of check for primarykey we create multiple endpoints
class ExperimentDetailView(APIView):
    """ """

    # To Do: add corresponding result if available
    permission_classes = (IsAuthenticated,)
    # serializers_class = serializers.ExperimentSerializer

    def get(self, request, experiment_id):
        """ """
        experiment = None
        experimentResult = None
        if experiment_id is not None:
            if request.user.is_staff:
                if models.Experiment.objects.filter(
                    experimentId=experiment_id
                ).exists():
                    # get targets experiment_id specified in URL
                    # not JSON id, or Project ID
                    experiment = models.Experiment.objects.get(
                        experimentId=experiment_id
                    )
                    # if ExperimentResult doesn't exist, else remains None
                    if models.ExperimentResult.objects.filter(
                        experiment=experiment
                    ).exists():
                        experimentResult = models.ExperimentResult.objects.get(
                            experiment=experiment
                        )
                else:
                    return Response(
                        "An Experiment with the specified ID was not found.",
                        status=status.HTTP_404_NOT_FOUND,
                    )
            # if enduser
            else:
                if models.Experiment.objects.filter(
                    experimentId=experiment_id,
                    # filtr also Experiment belongs to user
                    user=request.user,
                ).exists():
                    experiment = models.Experiment.objects.get(
                        experimentId=experiment_id,
                    )
                    if models.ExperimentResult.objects.filter(
                        experiment=experiment
                    ).exists():
                        experimentResult = models.ExperimentResult.objects.get(
                            experiment=experiment
                        )
                else:
                    return Response(
                        "An Experiment with the specified ID was not found or does not belong to the current user.",
                        status=status.HTTP_404_NOT_FOUND,
                    )

        # this is an if statement independent from the one above
        # logic returns required status messages according to api specs
        # print(experiment)
        if experiment is not None:
            if experimentResult is not None:
                experiment_serializer = serializers.ExperimentSerializer(
                    data=experiment,
                )
                experiment_serializer.is_valid()
                result_serializer = serializers.ExperimentResultSerializer(
                    data=experimentResult
                )
                result_serializer.is_valid()
                print(experiment_serializer.data)
                return Response(
                    {
                        "experimentConfiguration": experiment_serializer.data,
                        "experimentResult": result_serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )

            else:
                # if experiment is done, an ExperimentResult is also returned
                experiment_serializer = serializers.ExperimentSerializer(
                    experiment,
                )
                # experiment_serializer.is_valid()
                # print(experiment_serializer.data)
                return Response(
                    # {
                    #     "experimentConfiguration": experiment_serializer.data,
                    # },
                    experiment_serializer.data,
                    status=status.HTTP_200_OK,
                )
        else:
            # logic should not allow for this error to occur
            return Response(
                "Unexpected error.",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request, experiment_id):
        """ """

        if experiment_id is not None:
            if request.user.is_staff:
                if models.Experiment.objects.filter(
                    experimentId=experiment_id
                ).exists():
                    models.Experiment.objects.filter(
                        experimentId=experiment_id
                    ).delete()
                    return Response(
                        "OK - Experiment deleted successfully.",
                        status=status.HTTP_204_NO_CONTENT,
                    )
                else:
                    return Response(
                        "An Experiment with the specified ID was not found.",
                        status=status.HTTP_404_NOT_FOUND,
                    )
            else:
                if models.Experiment.objects.filter(
                    experimentId=experiment_id,
                    user=request.user,
                ).exists():
                    models.Experiment.objects.filter(
                        experimentId=experiment_id
                    ).delete()
                    return Response(
                        "OK - Experiment deleted successfully.",
                        status=status.HTTP_204_NO_CONTENT,
                    )
                else:
                    return Response(
                        "An Experiment with the specified ID was not found or does not belong to the current user.",
                        status=status.HTTP_404_NOT_FOUND,
                    )
        # 401 Authorization information is missing or invalid. is authomatically
        # handled with Django
        else:
            return Response(
                "Unexpected error.",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ExperimentListView(generics.ListCreateAPIView):
    """ """

    queryset = models.Experiment.objects.all()
    serializer_class = serializers.ExperimentSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        if request.user.is_staff:
            queryset = self.get_queryset()
        else:
            queryset = models.Experiment.objects.filter(user=request.user)
        serializer = serializers.ExperimentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ModelViewSet specifically designed for managing models through API
class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""

    serializer_class = serializers.UserProfileSerializer
    # Determine objects in the database which are managed in this view
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = (
        "name",
        "email",
    )


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""

    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES