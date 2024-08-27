from jira import JIRA

JIRA_URL = ""
JIRA_USER = ""
JIRA_PASSWORD = ""


class TicketManager:
    def __init__(self):
        self.jira = JIRA(JIRA_URL, basic_auth=(JIRA_USER, JIRA_PASSWORD))

    def get_projects(self):
        return self.jira.projects()

    def get_tickets(self, project_key: str):
        return self.jira.search_issues(f'project="{project_key}"')

    @staticmethod
    def ticket_status(ticket_):
        return ticket_.fields.status

    @staticmethod
    def ticket_reporter(ticket_):
        try:
            return ticket_.fields.reporter
        except AttributeError:
            return "Unknown"

    @staticmethod
    def ticket_assignee(ticket_):
        try:
            return ticket_.fields.assignee
        except AttributeError:
            return "Unknown"


if __name__ == '__main__':
    ticket_manager = TicketManager()
    projects = ticket_manager.get_projects()
    user = {}
    nb_total_tickets = 0
    for project in projects:
        tickets = ticket_manager.get_tickets(project.key)
        nb_total_tickets += len(tickets)
        for ticket in tickets:
            reporter = ticket_manager.ticket_reporter(ticket)
            assignee = ticket_manager.ticket_assignee(ticket)
            if assignee not in user:
                user[assignee] = {'ticket_to_do': 0, 'ticket_reported': 0}
            if reporter not in user:
                user[reporter] = {'ticket_to_do': 0, 'ticket_reported': 0}
            user[assignee]['ticket_to_do'] += 1
            user[reporter]['ticket_reported'] += 1

    print(f'There are {nb_total_tickets} tickets in total')
    user = dict(sorted(user.items(), key=lambda x: (x[1]['ticket_to_do'], x[1]['ticket_reported']), reverse=True))

    for name, value in user.items():
        print(f'{name} : {value["ticket_to_do"]} tickets to do, {value["ticket_reported"]} tickets reported')
