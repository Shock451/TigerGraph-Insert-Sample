import requests
import pyTigerGraph as tg
from dotenv import load_dotenv
import os
import ast

load_dotenv()

# host = os.environ.get('HOST')

conn = tg.TigerGraphConnection(
    host=os.environ.get('HOST'),
    password=os.environ.get('PASSWORD'),
    gsqlVersion=os.environ.get('GSQLVERSION'),
    graphname=os.environ.get('GRAPHNAME'),
    username=os.environ.get('USERNAME'),
    useCert=False
    # apiToken=os.environ.get('TOKEN')
)

conn.apiToken = conn.getToken(os.environ.get('TOKEN'))

headers = ast.literal_eval(os.environ.get('API_TOKEN'))

WORKSPACE_URL = 'https://not-gonna-happen.never/services/powerbi/workspaces'
REPORT_URL = 'https://not-gonna-happen.never/services/powerbi/workspaces/{}/reports'


def get_all_workspaces():
    res = requests.get(WORKSPACE_URL, headers=headers)
    if res.status_code == 200:
        return res.json()

    return []


def get_report(id):
    res = requests.get(REPORT_URL.format(id), headers=headers)
    if res.status_code == 200:
        return res.json()

    return []


def get_all_reports():

    data = []

    workspaces = get_all_workspaces()

    for workspace in workspaces:

        reports = get_report(workspace['id'])

        data.append({
            'reports': reports,
            'workspace_name': workspace['name'],
            'workspace_id': workspace['id']
        })

    return data


def upload_report_vertex(report):
    # insert vertex
    conn.upsertVertex(
        "report",  # name of vertex
        report["id"],  # id of this report
        attributes={
            # other attributes specified in the vertex's schema
            "id": report["id"],
            "name": report["name"],
            "webUrl": report["webUrl"],
            "embedUrl": report["embedUrl"],
            "datasetId": report["datasetId"]
        })


def upload_workspace_vertex(workspace):
    # insert vertex
    conn.upsertVertex(
        "workspace",  # name of vertex
        workspace["workspace_id"],  # id of this workspace
        attributes={
            # other attributes specified in the vertex's schema
            "id": workspace["workspace_id"],
            "name": workspace["workspace_name"]
        })


def connect_workspace_with_report(workspace_id, report_id):
    # connect this vertex (workspace) to the vertex
    conn.upsertEdge("report", report_id, "IN_WORKSPACE", "workspace", workspace_id)


def start_process():

    data = get_all_reports()

    # connect the vertex to the vertices of the workspaces using the IN_WORKSPACE relationship (edge)
    for workspace in data:

        upload_workspace_vertex(workspace)  # uploads the workspace

        for report in workspace['reports']:

            upload_report_vertex(report)  # uploads the report

            connect_workspace_with_report(workspace['workspace_id'], report['id'])

    print("Successful!")


start_process()
