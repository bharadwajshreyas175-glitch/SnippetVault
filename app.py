import os
from flask import Flask, render_template, request, redirect, url_for, Response
from datetime import datetime
import mysql.connector
from datetime import datetime
import mysql.connector
app = Flask(__name__)
def get_connection():
    return mysql.connector.connect(
        host=os.environ.get("MYSQLHOST", "localhost"),
        port=int(os.environ.get("MYSQLPORT", 3306)),
        user=os.environ.get("MYSQLUSER", "root"),
        password=os.environ.get("MYSQLPASSWORD", "shreyas"),
        database=os.environ.get("MYSQLDATABASE", "snippets_manager")
    )
# ==========================
# Welcome Page
# ==========================
@app.route("/")
def index():
    return render_template("index.html")


# ==========================
# Home Page
# ==========================
@app.route("/home", methods=["GET", "POST"])
def home():

    connection = get_connection() 
    cursor = connection.cursor()

    # Search and Filter values
    search = request.args.get("search")
    filter_language = request.args.get("language")

    # ==========================
    # Add New Snippet
    # ==========================
    if request.method == "POST":

        title = request.form["title"]
        snippet_language = request.form["language"]
        code = request.form["code"]
        description = request.form["description"]

        created_at = datetime.now().strftime("%d %b %Y | %I:%M %p")

        cursor.execute("""
    INSERT INTO snippets
    (title, language, code, description, created_at)
    VALUES (%s, %s, %s, %s, %s)
""", (
            title,
            snippet_language,
            code,
            description,
            created_at
        ))

        connection.commit()

    # ==========================
    # Search + Filter
    # ==========================

    if search and filter_language:

        cursor.execute("""
            SELECT * FROM snippets
            WHERE title LIKE %s
            AND language = %s
        """, ('%' + search + '%', filter_language))

    elif search:

     cursor.execute("""
        SELECT * FROM snippets
        WHERE
    title LIKE %s
    OR language LIKE %s
    OR description LIKE %s
    """, (
        '%' + search + '%',
        '%' + search + '%',
        '%' + search + '%'
    ))
    elif filter_language:

        cursor.execute("""
            SELECT * FROM snippets
           WHERE language = %s
        """, (filter_language,))

    else:

        cursor.execute("""
            SELECT * FROM snippets
        """)

    snippets = cursor.fetchall()

    total_snippets = len(snippets)
    # Language Counts
    cursor.execute("SELECT COUNT(*) FROM snippets WHERE language='Python'")
    python_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM snippets WHERE language='Java'")
    java_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM snippets WHERE language='C++'")
    cpp_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM snippets WHERE language='JavaScript'")
    javascript_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM snippets WHERE language='HTML'")
    html_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM snippets WHERE language='CSS'")
    css_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM snippets WHERE language='SQL'")
    sql_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM snippets WHERE language='C'")
    c_count = cursor.fetchone()[0]

    connection.close()

    return render_template(
    "home.html",
    snippets=snippets,
    total_snippets=total_snippets,
    python_count=python_count,
    java_count=java_count,
    cpp_count=cpp_count,
    javascript_count=javascript_count,
    html_count=html_count,
    css_count=css_count,
    sql_count=sql_count,
    c_count=c_count
)


# ==========================
# Edit Snippet
# ==========================
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    connection = get_connection()
    cursor = connection.cursor()

    if request.method == "POST":

        title = request.form["title"]
        language = request.form["language"]
        code = request.form["code"]
        description = request.form["description"]

        cursor.execute("""
            UPDATE snippets
            SET
               title=%s,
language=%s,
code=%s,
description=%s
WHERE id=%s
        """, (
            title,
            language,
            code,
            description,
            id
        ))

        connection.commit()
        connection.close()

        return redirect(url_for("home"))

    cursor.execute(
    "SELECT * FROM snippets WHERE id=%s",
    (id,)
)

    snippet = cursor.fetchone()

    connection.close()

    return render_template("edit.html", snippet=snippet)


# ==========================
# Delete Snippet
# ==========================
@app.route("/delete/<int:id>")
def delete(id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
    "DELETE FROM snippets WHERE id=%s",
    (id,)
)
    connection.commit()
    connection.close()

    return redirect(url_for("home"))


# ==========================
# Download Snippet
# ==========================
@app.route("/download/<int:id>")
def download(id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT title, language, code, description
        FROM snippets
        WHERE id=%s
    """, (id,))

    snippet = cursor.fetchone()

    connection.close()

    if snippet:

        title = snippet[0]
        language = snippet[1]
        code = snippet[2]
        description = snippet[3]

        content = f"""Title: {title}

Language: {language}

Description:
{description}

----------------------------------------

Code:

{code}
"""

        return Response(
            content,
            mimetype="text/plain",
            headers={
                "Content-Disposition":
                f'attachment; filename="{title.replace(" ", "_")}.txt"'
            }
        )

    return "Snippet not found."

# ==========================
# Add Snippet Page
# ==========================
@app.route("/add")
def add_page():
    return render_template("add.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)