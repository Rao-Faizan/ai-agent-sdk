import json

def answer_question(question, data_file="ait_data.json"):
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        title = data.get('title', '')
        paragraphs = data.get("paragraphs", [
            "AIT is a nonprofit NGO that provides free IT and vocational courses to students. It aims to empower youth through technology and education.",
            "AIT is located in Karachi, Pakistan. It offers both online and onsite classes to facilitate learners from different regions.",
            "The owner and founder of AIT is Mr. Javed Iqbal, who is committed to spreading quality technical education free of cost.",
            "The institute runs under Idara Al Khair, a well-known social welfare organization that has been serving communities for years.",
            "AIT offers a wide range of courses including: Web Development, App Development, Cybersecurity, Game Development, Mobile App Development, Data Science, Artificial Intelligence, Graphic Designing, Video Editing, WordPress Development, Freelancing, and more.",
            "All courses at AIT are free. However, students are required to deposit a refundable security fee at the time of admission. This fee is returned upon successful completion of the course.",
            "AIT’s mission is to bridge the gap between underprivileged communities and technology by providing free, high-quality IT education.",
            "AIT’s vision is to build a self-sustainable, tech-literate society by nurturing skilled individuals who can contribute to the national economy.",
            "The institute promotes gender equality, encouraging both boys and girls to pursue education and build a career in tech.",
            "Courses are designed and taught by experienced industry professionals and mentors with hands-on practical training.",
            "AIT regularly updates its course content according to modern industry standards and student needs."
        ])

        # Simple keyword matching
        question = question.lower()
        for paragraph in paragraphs:
            if question in paragraph.lower():
                return paragraph
        if question in title.lower():
            return title
        return "I'm sorry, I couldn't find an answer to your question in the scraped data."

    except FileNotFoundError:
        return "Error: The data file 'ait_data.json' was not found."
    except json.JSONDecodeError:
        return "Error: The data file 'ait_data.json' is not a valid JSON file."
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    question = input("Ask a question: ")
    answer = answer_question(question)
    print(answer)
