from flask import *
import pyTigerGraph as tg
from dotenv import load_dotenv
import os

load_dotenv()

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

app = Flask(__name__)


@app.route("/report", methods=['POST'])
def report():
    if request.method == 'POST':
        report = request.get_json()

        # insert vertex
        conn.upsertVertex(
            "report",  # name of vertex
            report["id"],  # id of this report
            attributes={
                # other attributes specified in the vertex's schema
                "name": report["name"],
                "synonyms": report["synonyms"]
            })

        # connect the vertex to the vertices of the workspaces using the IN_WORKSPACE relationship (edge)
        for workspace in report["workspaces"]:
            # insert the workspace vertex
            conn.upsertVertex("workspace", workspace["id"])

            # connect this vertex (workspace) to the vertex (report) inserted earlier
            conn.upsertEdge(
                "report",
                report["id"],
                "IN_WORKSPACE",
                "workspace",
                workspace["id"])

        print("Successful")

        return jsonify({'success': True})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3300, debug=True)
