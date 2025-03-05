"""
Test résumé data for development and testing purposes.
This file contains the résumé information from the project prompt.
"""

RESUME_DATA = {
    "name": "Nick Krzemienski",
    "title": "Engineering Lead, Video Innovations @ fuboTV",
    "summary": """
    • Over 12 years of experience in software engineering management and technical leadership.
    • Transitioned into the OTT video space in 2016, expanding expertise in mobile and web development.
    • Pioneered a shared Swift library for iOS/tvOS apps, separating the UI from the player for scalability.
    • Spearheaded major initiatives at fuboTV, including transformation of tvOS/Roku, in-house VOD encoding, and server-side multi-view systems.
    • Led just-in-time transcoding solutions deployed in Kubernetes.
    • Extensive experience in FFmpeg research, ISO standards, encoding workflows, AWS, Docker, and continuous software enhancements.
    • Former Squad Leader in the United States Marine Corps Reserve, emphasizing duty and strategic execution.
    """,
    "core_experience": [
        "Engineering Lead, Video Innovations, fuboTV Inc.",
        "Engineering Lead, VOD Encoding & Operations, fuboTV Inc.",
        "Engineering Manager, AppleTV & Roku, fuboTV Inc.",
        "Software Engineer, iOS, fuboTV Inc.",
        "Principal Developer & Founder, KODA LABS INC.",
        "Squad Leader, United States Marine Corps Reserve",
        "Founder & Managing Director for various projects",
        "Mobile Developer, SHODOGG",
        "Ops Intern, Argus Information and Advisory Services"
    ],
    "education": [
        "Bachelor of Computer Science, Iona College"
    ],
    "contact_info": {
        "email": "krzemienski@gmail.com",
        "twitter": "twitter.com/nkrzemienski"
    },
    "portfolio": {
        "website": "awesome.video",
        "github": "github.com/krzemienski"
    }
}

# Function to get the résumé data
def get_resume_data():
    """Return the test résumé data."""
    return RESUME_DATA
