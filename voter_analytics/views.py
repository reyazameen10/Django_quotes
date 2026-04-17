#reyam/ voter_analytics/views.py 

from django.views.generic import ListView, DetailView
from .models import Voter
from datetime import datetime
import plotly.express as px
from django.utils.safestring import mark_safe

# helper so we don't repeat filtering logic twice
def apply_filters(qs, GET):
    '''Apply GET filter params to a Voter queryset and return it.'''
    party      = GET.get('party')
    min_dob    = GET.get('min_dob')
    max_dob    = GET.get('max_dob')
    score      = GET.get('voter_score')

    if party:
        qs = qs.filter(party_affiliation=party)
    if min_dob:
        qs = qs.filter(date_of_birth__year__gte=min_dob) 
    if max_dob:
        qs = qs.filter(date_of_birth__year__lte=max_dob) 
    if score:
        qs = qs.filter(voter_score=score)

    for election in ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']:
        if GET.get(election):
            qs = qs.filter(**{election: True})

    return qs

# we need the class for voterslistview
class VoterListView(ListView):
    '''Display a paginated, filterable list of Voters.'''
    model            = Voter
    template_name    = 'voter_analytics/voters.html'
    context_object_name = 'voters'
    paginate_by      = 100

    def get_queryset(self):
        '''Return filtered and ordered Voter queryset.'''
        qs = super().get_queryset().order_by('last_name')
        return apply_filters(qs, self.request.GET)

    def get_context_data(self, **kwargs):
        '''Add filter dropdown data to context.'''
        context = super().get_context_data(**kwargs)
        context['years']   = range(1920, datetime.now().year + 1)
        context['parties'] = Voter.objects.values_list(
                                'party_affiliation', flat=True).distinct()
        #from prev form
        context['selected_party']      = self.request.GET.get('party', '')
        context['selected_min_dob']    = self.request.GET.get('min_dob', '')
        context['selected_max_dob']    = self.request.GET.get('max_dob', '')
        context['selected_score']      = self.request.GET.get('voter_score', '')
        return context


class VoterDetailView(DetailView):
    '''Display all fields for a single Voter.'''
    model            = Voter
    template_name    = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'


class GraphView(ListView):
    '''Display plotly graphs of filtered Voter data.'''
    model            = Voter
    template_name    = 'voter_analytics/graphs.html'
    context_object_name = 'voters'
    paginate_by      = None   # that part I had a lot of issue, be careful here

    def get_queryset(self):
        '''Return filtered Voter queryset for graphing.'''
        qs = super().get_queryset().order_by('last_name')
        return apply_filters(qs, self.request.GET)

    def get_context_data(self, **kwargs):
        '''Build plotly graphs and add to context.'''
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset()  #use full queryset, not paginated

        # 1. Birth Year Histogram
        years = [v.date_of_birth.year for v in qs if v.date_of_birth]
        fig1  = px.histogram(x=years, nbins=50, title="Birth Year Distribution",
                             labels={'x': 'Year', 'y': 'Count'})
        context['graph1'] = mark_safe(fig1.to_html(full_html=False))

        # 2. Party Pie Chart
        parties = {}
        for v in qs:
            p = v.party_affiliation.strip()
            parties[p] = parties.get(p, 0) + 1
        fig2 = px.pie(names=list(parties.keys()),
                      values=list(parties.values()),
                      title="Party Affiliation Distribution")
        context['graph2'] = mark_safe(fig2.to_html(full_html=False))

        # 3. Election Participation Bar Chart
        elections = {
            '2020 State':   qs.filter(v20state=True).count(),
            '2021 Town':    qs.filter(v21town=True).count(),
            '2021 Primary': qs.filter(v21primary=True).count(),
            '2022 General': qs.filter(v22general=True).count(),
            '2023 Town':    qs.filter(v23town=True).count(),
        }
        fig3 = px.bar(x=list(elections.keys()),
                      y=list(elections.values()),
                      title="Voter Participation by Election",
                      labels={'x': 'Election', 'y': 'Voters'})
        context['graph3'] = mark_safe(fig3.to_html(full_html=False))

        # dropdown data
        context['years']   = range(1920, datetime.now().year + 1)
        context['parties'] = Voter.objects.values_list(
                                'party_affiliation', flat=True).distinct()
        # keep previously selected values
        context['selected_party']   = self.request.GET.get('party', '')
        context['selected_min_dob'] = self.request.GET.get('min_dob', '')
        context['selected_max_dob'] = self.request.GET.get('max_dob', '')
        context['selected_score']   = self.request.GET.get('voter_score', '')
        return context