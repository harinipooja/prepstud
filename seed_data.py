"""Populate the database with sample aptitude, coding, and interview content."""

from models import AptitudeQuestion, CodingProblem, InterviewQuestion, db


def seed_all() -> None:
    if AptitudeQuestion.query.first():
        return

    aptitude = [
        AptitudeQuestion(
            category="Quantitative",
            question="A train 120 m long passes a pole in 12 seconds. What is its speed in km/h?",
            option_a="36",
            option_b="40",
            option_c="42",
            option_d="45",
            correct_option="A",
            explanation="Speed = 120/12 = 10 m/s = 10 × 18/5 = 36 km/h.",
        ),
        AptitudeQuestion(
            category="Quantitative",
            question="If 20% of a number is 60, what is 40% of the same number?",
            option_a="100",
            option_b="120",
            option_c="140",
            option_d="160",
            correct_option="B",
            explanation="20% = 60 ⇒ number = 300. 40% of 300 = 120.",
        ),
        AptitudeQuestion(
            category="Quantitative",
            question="The average of 5 numbers is 40. If one number is excluded, the average becomes 38. What is the excluded number?",
            option_a="46",
            option_b="48",
            option_c="50",
            option_d="52",
            correct_option="B",
            explanation="Total = 200. Remaining total = 152. Excluded = 48.",
        ),
        AptitudeQuestion(
            category="Quantitative",
            question="Simple interest on ₹5000 at 10% per annum for 2 years is:",
            option_a="₹800",
            option_b="₹900",
            option_c="₹1000",
            option_d="₹1100",
            correct_option="C",
            explanation="SI = PRT/100 = 5000×10×2/100 = 1000.",
        ),
        AptitudeQuestion(
            category="Quantitative",
            question="A shopkeeper marks an item 40% above cost and gives 10% discount. Profit % is:",
            option_a="26%",
            option_b="28%",
            option_c="30%",
            option_d="32%",
            correct_option="A",
            explanation="SP = 1.4 × 0.9 = 1.26 → 26% profit.",
        ),
        AptitudeQuestion(
            category="Logical",
            question="Find the odd one out: 3, 5, 11, 14, 17, 21",
            option_a="21",
            option_b="17",
            option_c="14",
            option_d="3",
            correct_option="C",
            explanation="All others are prime numbers; 14 is not.",
        ),
        AptitudeQuestion(
            category="Logical",
            question="If CAT = 24 and DOG = 26, then BAT = ?",
            option_a="23",
            option_b="22",
            option_c="21",
            option_d="20",
            correct_option="A",
            explanation="Sum of positions: B(2)+A(1)+T(20)=23.",
        ),
        AptitudeQuestion(
            category="Logical",
            question="Complete the series: 2, 6, 12, 20, 30, ?",
            option_a="40",
            option_b="42",
            option_c="44",
            option_d="46",
            correct_option="B",
            explanation="Differences are +4,+6,+8,+10,+12 → next is 42.",
        ),
        AptitudeQuestion(
            category="Logical",
            question="All roses are flowers. Some flowers fade quickly. Conclusion: Some roses fade quickly.",
            option_a="True",
            option_b="False",
            option_c="Cannot be determined",
            option_d="Partially true",
            correct_option="C",
            explanation="The roses may or may not be among flowers that fade.",
        ),
        AptitudeQuestion(
            category="Logical",
            question="Pointing to a photo, Ravi said, 'She is the daughter of my grandfather's only son.' How is she related to Ravi?",
            option_a="Sister",
            option_b="Mother",
            option_c="Cousin",
            option_d="Aunt",
            correct_option="A",
            explanation="Grandfather's only son is Ravi's father; she is his sister.",
        ),
        AptitudeQuestion(
            category="Verbal",
            question="Choose the synonym of 'Diligent':",
            option_a="Lazy",
            option_b="Hardworking",
            option_c="Careless",
            option_d="Rude",
            correct_option="B",
            explanation="Diligent means showing care and hard work.",
        ),
        AptitudeQuestion(
            category="Verbal",
            question="Choose the antonym of 'Benevolent':",
            option_a="Kind",
            option_b="Generous",
            option_c="Malevolent",
            option_d="Friendly",
            correct_option="C",
            explanation="Benevolent means kind; malevolent means wishing harm.",
        ),
        AptitudeQuestion(
            category="Verbal",
            question="Identify the correctly spelled word:",
            option_a="Accomodate",
            option_b="Acommodate",
            option_c="Accommodate",
            option_d="Acomodate",
            correct_option="C",
            explanation="Correct spelling is Accommodate (double c, double m).",
        ),
        AptitudeQuestion(
            category="Verbal",
            question="Fill in the blank: She has been working here _____ 2019.",
            option_a="for",
            option_b="since",
            option_c="from",
            option_d="by",
            correct_option="B",
            explanation="'Since' is used with a point in time.",
        ),
        AptitudeQuestion(
            category="Verbal",
            question="Choose the correctly punctuated sentence:",
            option_a="Its a beautiful day.",
            option_b="It's a beautiful day.",
            option_c="Its' a beautiful day.",
            option_d="It a beautiful day.",
            correct_option="B",
            explanation="It's = it is.",
        ),
    ]

    coding = [
        CodingProblem(
            title="Sum of Two Numbers",
            difficulty="Easy",
            description=(
                "Read two integers A and B from input (space-separated) and print their sum.\n\n"
                "Input format: A B\nOutput: A single integer — the sum."
            ),
            sample_input="3 5",
            sample_output="8",
            hints="Use input().split() and map to int, then print a+b.",
            starter_code="a, b = map(int, input().split())\n# write your code\n",
            test_input="3 5\n10 20\n0 0\n-2 7",
            test_output="8\n30\n0\n5",
        ),
        CodingProblem(
            title="Even or Odd",
            difficulty="Easy",
            description=(
                "Read an integer N and print 'Even' if it is even, otherwise print 'Odd'."
            ),
            sample_input="7",
            sample_output="Odd",
            hints="Use modulo operator: n % 2 == 0.",
            starter_code="n = int(input())\n# write your code\n",
            test_input="7\n4\n0\n-3",
            test_output="Odd\nEven\nEven\nOdd",
        ),
        CodingProblem(
            title="Factorial",
            difficulty="Medium",
            description=(
                "Read a non-negative integer N and print N! (factorial of N).\n"
                "0! = 1."
            ),
            sample_input="5",
            sample_output="120",
            hints="Use a loop or math.factorial. Handle 0 carefully.",
            starter_code="n = int(input())\n# write your code\n",
            test_input="5\n0\n1\n6",
            test_output="120\n1\n1\n720",
        ),
        CodingProblem(
            title="Reverse a String",
            difficulty="Easy",
            description="Read a string and print it reversed.",
            sample_input="hello",
            sample_output="olleh",
            hints="Use slicing: s[::-1]",
            starter_code="s = input().strip()\n# write your code\n",
            test_input="hello\nabc\nPlacement",
            test_output="olleh\ncba\ntnemecalP",
        ),
        CodingProblem(
            title="Maximum of Three",
            difficulty="Easy",
            description="Read three integers and print the largest one.",
            sample_input="4 9 2",
            sample_output="9",
            hints="Use max(a, b, c).",
            starter_code="a, b, c = map(int, input().split())\n# write your code\n",
            test_input="4 9 2\n10 10 5\n-1 -5 -3",
            test_output="9\n10\n-1",
        ),
        CodingProblem(
            title="Count Vowels",
            difficulty="Medium",
            description=(
                "Read a string and print the count of vowels (a, e, i, o, u — case insensitive)."
            ),
            sample_input="Education",
            sample_output="5",
            hints="Convert to lowercase and count characters in 'aeiou'.",
            starter_code="s = input().strip()\n# write your code\n",
            test_input="Education\nPython\nxyz",
            test_output="5\n1\n0",
        ),
    ]

    interview = [
        InterviewQuestion(
            category="HR",
            question="Tell me about yourself.",
            model_answer=(
                "Start with your education, highlight 1–2 relevant projects or internships, "
                "mention key skills matching the role, and end with why you are interested in this company."
            ),
            tips="Keep it under 2 minutes. Avoid reading your resume line by line.",
        ),
        InterviewQuestion(
            category="HR",
            question="Why should we hire you?",
            model_answer=(
                "Connect your skills to the job requirements. Mention a concrete achievement "
                "(project, internship metric) and show enthusiasm for contributing to the team."
            ),
            tips="Be confident but not arrogant. Use the STAR approach if you share an example.",
        ),
        InterviewQuestion(
            category="HR",
            question="What are your strengths and weaknesses?",
            model_answer=(
                "Strength: pick one real strength with an example. Weakness: pick something "
                "improvable (e.g., public speaking) and show what you are doing to improve it."
            ),
            tips="Never say 'I have no weakness' or a fake weakness like 'I work too hard'.",
        ),
        InterviewQuestion(
            category="Behavioral",
            question="Describe a time you faced a conflict in a team and how you resolved it.",
            model_answer=(
                "Use STAR: Situation, Task, Action, Result. Focus on communication, compromise, "
                "and a positive outcome for the project."
            ),
            tips="Interviewers look for maturity and collaboration, not blame.",
        ),
        InterviewQuestion(
            category="Behavioral",
            question="Tell me about a project you are most proud of.",
            model_answer=(
                "Explain the problem, your role, technologies used, challenges, and measurable results "
                "(users, performance, marks, GitHub stars, etc.)."
            ),
            tips="Be ready for deep follow-up questions on your tech choices.",
        ),
        InterviewQuestion(
            category="Technical",
            question="Explain the difference between a process and a thread.",
            model_answer=(
                "A process is an independent program with its own memory space. "
                "Threads are lightweight units within a process that share memory. "
                "Context switching between threads is usually cheaper than between processes."
            ),
            tips="Mention shared memory and synchronization briefly.",
        ),
        InterviewQuestion(
            category="Technical",
            question="What is the difference between TCP and UDP?",
            model_answer=(
                "TCP is connection-oriented, reliable, ordered, and slower. "
                "UDP is connectionless, faster, unordered, and does not guarantee delivery. "
                "Use TCP for file transfer/web; UDP for streaming/gaming."
            ),
            tips="Give one real-world example for each.",
        ),
        InterviewQuestion(
            category="Technical",
            question="Explain OOP concepts: encapsulation, inheritance, polymorphism.",
            model_answer=(
                "Encapsulation: bundling data with methods and hiding internals. "
                "Inheritance: a class derives properties from another. "
                "Polymorphism: same interface, different implementations (overloading/overriding)."
            ),
            tips="Give a short code-level example if asked.",
        ),
        InterviewQuestion(
            category="Technical",
            question="What is the time complexity of binary search?",
            model_answer=(
                "O(log n) for searching in a sorted array, because each step halves the search space."
            ),
            tips="Mention the prerequisite: the array must be sorted.",
        ),
        InterviewQuestion(
            category="Technical",
            question="Difference between SQL and NoSQL databases?",
            model_answer=(
                "SQL databases are relational with fixed schemas and ACID transactions (MySQL, PostgreSQL). "
                "NoSQL databases are flexible (document, key-value, etc.) and scale horizontally more easily "
                "(MongoDB, Redis)."
            ),
            tips="Say when you would choose each based on use case.",
        ),
    ]

    db.session.add_all(aptitude + coding + interview)
    db.session.commit()
