from data import OpenDataRequests


class OpenDataParliamentariansPayments(object):
    def dump(self):
        payments = OpenDataRequests.get_parliamentarians_json()
        return payments
