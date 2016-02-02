from flask import Flask, render_template, request, redirect, url_for, flash
from serverprocessing import ServerProcessing

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('table.html')

@app.route('/getData')
def getData():
    sEcho = request.args.get("sEcho")
    sSortDir = request.args.get("sSortDir_0")
    sortCol = request.args.get("iSortCol_0")
    displayStart = request.args.get("iDisplayStart")
    search = request.args.get("sSearch")
    sortingCol = request.args.get("sortingCols")
    displayLength = request.args.get("iDisplayLength")

    data = ServerProcessing()
    data.setDataTableOptions( sEcho,sSortDir,sortCol,displayStart,search,sortingCol,displayLength) #echo sortdir sortcol displaystart search sortingcolumns displaylength
    return data.getDataTableData()


if __name__ == '__main__':
    app.run(debug=True)
