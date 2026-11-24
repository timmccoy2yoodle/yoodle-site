# Content data for yoodle.com. Facts come from each live site (read Nov 23, 2026) or from Tim.
# Anything Yoodle-specific that is not yet verified is rendered as an amber CONFIRM tag.

SECTORS = {
    "higher-ed": ("Higher education", "#2c2a6f"),
    "government": ("Government", "#111110"),
    "nonprofit": ("Nonprofit", "#783a92"),
    "business": ("Small business", "#953c92"),
    "content": ("Podcasts", "#b0326f"),
}

# slug, name, sector, url, place, platform, about, features, kind
P = []
def add(slug, name, sector, url, place, platform, about, features, kind="Website"):
    P.append(dict(slug=slug, name=name, sector=sector, url=url, place=place, platform=platform,
                  about=about, features=features, kind=kind))

# ---- Higher education
add("nevada-state-university", "Nevada State University", "higher-ed", "https://nevadastate.edu/", "Henderson, Nevada", "WordPress",
    "Nevada State University is Nevada's four-year teaching institution. Its website has to serve current students, prospective students, alumni, and parents and families from one front door.",
    ["Audience paths for current students, prospective students, alumni, and parents and families", "Degrees and programs listing", "Class search and catalog links", "Events calendar and news", "Tour scheduling and application links"])
add("san-bernardino-community-college-district", "San Bernardino Community College District", "higher-ed", "https://sbccd.edu/", "San Bernardino, California", "Modern Campus CMS (OmniUpdate)",
    "SBCCD is the district behind Crafton Hills College, San Bernardino Valley College, KVCR public media and the Economic Development and Corporate Training Center. The district site carries governance, bond and business information for the whole system.",
    ["Board of Trustees meetings and agendas", "Citizens Bond Oversight Committee and bid opportunities", "District services and staff directory", "Careers", "District news"])
add("compton-college", "Compton College", "higher-ed", "https://compton.edu/", "Compton, California", "",
    "Compton College is a California community college whose homepage leads with one idea: every student is a success story.",
    ["Start Here path for first-time students", "Guided Pathways program explorer", "Student life, clubs and activities", "Calendar and important dates", "Spanish-language section for ESL learners", "Student success stories"])
add("rio-hondo-college", "Río Hondo College", "higher-ed", "https://www.riohondo.edu/", "Whittier, California", "WordPress",
    "Río Hondo College serves first-time, returning, transfer, international, continuing education and dual enrollment students in southeast Los Angeles County.",
    ["Paths for six student types", "Find Your Program and areas of study", "Virtual Welcome Center", "Class schedule and registration links", "News Hub, events calendar and key dates"])
add("ut-austin-extended-campus", "UT Austin Extended Campus", "higher-ed", "https://extendedcampus.utexas.edu/", "Austin, Texas", "Drupal",
    "Extended Campus is the continuing and professional education unit of The University of Texas at Austin. Its site helps working adults find a program by type, subject and format.",
    ["Program Finder with filters for program type, area of interest and format", "Custom training for organizations", "Free events and FAQs for new learners", "Career Insights blog and faculty spotlights"])
add("earth-center", "The EARTh Center", "higher-ed", "https://earthcntr.org/", "Sanford, North Carolina", "Drupal",
    "The EARTh Center is the Environmental and Natural Resources Technology Center, a National Science Foundation Advanced Technological Education center that supports environmental technology programs at colleges.",
    ["Immersive Ed Center with instructional videos and simulations", "Job Task Analysis Tool", "Media library and Environmental Tech Map", "DACUM examples and a best practice guide for programs", "Events and newsletter signup"])
add("fsu-career-center", "Florida State University Career Center", "higher-ed", "https://career.fsu.edu/", "Tallahassee, Florida", "Drupal",
    "The FSU Career Center, part of the Division of Student Affairs, connects students, employers, and faculty and staff. The homepage opens by asking each visitor what brings them there.",
    ["Separate paths for students, employers, and faculty and staff", "Career fairs and events", "NoleNetwork job board", "Career advising, resume and interview help", "Graduate outcome data"])
add("cochise-college", "Cochise College", "higher-ed", "https://www.cochise.edu/", "Cochise County, Arizona", "Modern Campus CMS (OmniUpdate)",
    "Cochise College serves southeast Arizona from Douglas, Sierra Vista, Benson, Willcox and Fort Huachuca, plus online.",
    ["Paths for first-time, high school, adult education, returning, military and international students", "Degree and certificate Program Finder", "Site search", "Featured events and news", "Workforce training"])
add("crowder-college", "Crowder College", "higher-ed", "https://www.crowder.edu/", "Neosho, Missouri", "WordPress",
    "Crowder College is a community college in southwest Missouri with a plain promise on its homepage: changing lives and strengthening communities, one student at a time.",
    ["Paths for prospective students, faculty and staff, parents and family, and alumni", "Program finder", "Events and news", "Course schedule and catalog links", "Foundation and giving"])
add("palm-beach-state-college", "Palm Beach State College", "higher-ed", "https://pbsc.edu/", "Palm Beach County, Florida", "",
    "Palm Beach State College opens with \"A Smart Start\" and walks new students from first question to first class.",
    ["Where to Start guide", "Career Pathways with pathway maps", "Important dates", "Featured news and upcoming events", "Student success spotlights"])
add("miracosta-college", "MiraCosta College", "higher-ed", "https://miracosta.edu/", "Oceanside, California", "Modern Campus CMS (OmniUpdate)",
    "MiraCosta College serves coastal North San Diego County from campuses in Oceanside and Cardiff, and a technology career institute in Carlsbad.",
    ["Paths for new, returning, international, high school and noncredit students", "Program finder and Career Coach", "Site search", "Virtual campus tours", "News and events"])
add("missouri-western-state-university", "Missouri Western State University", "higher-ed", "https://www.missouriwestern.edu/", "St. Joseph, Missouri", "",
    "Missouri Western State University chose Yoodle through a public RFP for market research and brand development. The work grew into a rebrand, a marketing campaign and advertising. Yoodle designed the new MO West logo.",
    ["Brand perception research: internal, community and prospective-student studies", "Brand strategy", "Communication audit and creative concept", "The MO West logo: a primary mark, a stacked mark and secondary MW and MO West marks, approved by the university in November 2024", "\"More at MO West\" campaign creative for outdoor and social", "Campaign and marketing plan", "Brand launch video, 2025", "Ongoing marketing support on retainer, 2024 to 2025"], "Brand and marketing")
P[-1]["gallery"] = [("The primary MO West logo, in black and in white", 1448, 807), ("The stacked MO West logo", 1448, 807), ("Secondary marks: MW with the griffon, W MO West and MO West", 1448, 807), ("More at MO West campaign banners", 1448, 807), ("More at MO West social posts", 1448, 807)]
add("ci3t", "Ci3T", "higher-ed", "https://www.ci3t.org/", "", "WordPress",
    "Ci3T (Comprehensive, Integrated, Three-Tiered Model of Prevention) is a research-based framework that helps school leaders bring academics, behavior and social-emotional well-being into one system.",
    ["40+ professional learning modules", "Design, Implement, and Measures and Tools sections", "Presentations archive and research", "Events", "My Ci3T account area"])
add("swift-education-center", "SWIFT Education Center", "higher-ed", "https://swiftschools.org", "University of Kansas", "WordPress",
    "SWIFT Education Center at the University of Kansas is a research and services organization focused on equity-based multi-tiered systems of support for schools.",
    ["Resource library", "Research and stories", "How SWIFT Works", "Newsletter signup", "WCAG 2.1 AA accessibility audit, fixes, retest and certification by Yoodle in fall 2026"])
add("missouri-kinship-navigator", "Missouri Kinship Navigator", "higher-ed", "https://www.mokin4kid.org/", "University of Missouri", "Drupal",
    "MO KIN-4-KID is the Missouri Kinship Navigator Program, run by ParentLink at the University of Missouri. It supports relatives who are raising children across the state.",
    ["Caregiver checklists", "Legal information", "Education and support events by Zoom or phone", "Resources by need", "Call, email and text contact options"])

# ---- Government
add("kansas-judicial-branch", "Kansas Judicial Branch", "government", "https://kscourts.gov/", "Topeka, Kansas", "",
    "kscourts.gov is the website of the Kansas Judicial Branch: the district courts, the Court of Appeals and the Supreme Court. Attorneys, self-represented people, jurors and the press all rely on it.",
    ["eFiling login for Kansas attorneys", "Live and archived Supreme Court oral arguments", "Travel docket notices", "Find a District Court"])
add("multistate-tax-commission", "Multistate Tax Commission", "government", "https://mtc.gov", "Washington, D.C.", "WordPress",
    "The Multistate Tax Commission is an intergovernmental state tax agency that promotes uniform tax policy and helps taxpayers comply with state tax laws.",
    ["Uniformity projects", "National Nexus Program", "Audit program resources", "Events and training, with an online learning center", "Amicus briefs and committee meetings"])
add("neighborworks-america", "NeighborWorks America", "government", "https://www.neighborworks.org/", "Washington, D.C.", "",
    "NeighborWorks America is a congressionally chartered national nonprofit that supports nearly 250 local organizations working on affordable housing and community development in every state.",
    ["Grants, training and technical assistance for the network", "\"Working Together for Strong Communities\" brand front door"])
add("kc-streetcar", "KC Streetcar", "government", "https://kcstreetcar.org/", "Kansas City, Missouri", "WordPress",
    "KC Streetcar is Kansas City's free electric streetcar, running 6.5 miles from the Riverfront to UMKC. Riders use the site on their phones, at the stop.",
    ["Route, hours and parking", "Arrival times and streetcar tracker", "Text alerts", "Accessibility and ADA pages", "Ridership data, board meetings and RFPs"])

# ---- Nonprofit
add("marc-head-start", "MARC Head Start", "nonprofit", "https://marcheadstart.org/", "Kansas City, Missouri", "WordPress",
    "MARC Head Start, a program of the Mid-America Regional Council, serves more than 2,400 infants, toddlers, preschoolers and their families in Clay, Jackson and Platte counties.",
    ["Eligibility information and applications by appointment", "Provider locator", "Paths for families and for providers", "Family success stories", "Careers, volunteering and giving"])
add("music-theater-heritage", "Music Theater Heritage", "nonprofit", "https://musictheaterheritage.com/", "Kansas City, Missouri", "WordPress",
    "Music Theater Heritage is a nonprofit professional theater company at Crown Center that produces musicals, cabarets, concerts and original revues.",
    ["Show listings and calendar", "Ticketing, season tickets and gift cards", "Education programs and summer camps", "Donations and monthly giving", "Theater trips and volunteer signup"])
add("variety-socal", "Variety of Southern California", "nonprofit", "https://varietysocal.org/", "Los Angeles, California", "WordPress",
    "Variety, the Children's Charity of Southern California, serves children with disabilities and their families across the region.",
    ["Grant information", "Family stories", "Events", "Volunteer signup", "Donation flow with a monthly option"])
add("variety-kc", "Variety KC", "nonprofit", "https://varietykc.org/", "Kansas City, Missouri", "WordPress",
    "Variety KC, the Children's Charity of Kansas City, funds mobility equipment, assistive technology and therapy, and builds inclusive parks and playgrounds so every kid can be active, be social and belong.",
    ["Grant applications", "Family resources directory", "Event pages and calendar", "Inclusion map", "Donations, monthly giving and shop"])

# ---- Small business
add("wentworth-financial-communications", "Wentworth Financial Communications", "business", "https://wentworthwriting.com/", "Chicago, Illinois", "WordPress",
    "Wentworth Financial Communications is a content marketing firm for asset managers, wealth managers and investment banks. The site sells one thing: investment-grade writing.",
    ["Who We Are, What We Do and Industry Focus", "Portfolio of white papers, e-books, videos and infographics", "Blog", "Newsletter signup"])
add("dr-amy-k-patel", "Dr. Amy K. Patel", "business", "https://dramykpatel.com/", "Kansas City, Missouri", "WordPress",
    "Dr. Amy K. Patel is a breast imaging radiologist and national voice on breast health. Her site helps patients take charge of their breast health.",
    ["Patient support and second opinions", "#ASKAMYMD questions and answers", "In The Know: blog, media features and published articles", "Newsletter signup"])
add("savvy-bridal", "Savvy Bridal", "business", "https://savvybridalboutique.com/", "Kansas City, St. Louis and Fort Lauderdale", "Static site on Netlify",
    "Savvy Bridal is a family-owned bridal boutique, established in 2013, with private styling suites in three cities. Yoodle's own leadership runs its marketing, so this site is where we test what we sell.",
    ["Appointment booking for each location", "Designer directory", "Off-the-rack and plus-size pages", "A tool that works out a \"say yes\" date from the wedding date", "Blog and gown preservation service"])
add("nick-and-jakes", "Nick and Jake's", "business", "https://nickandjakes.com/", "Overland Park, Shawnee and Parkville", "Static site on Netlify",
    "Nick and Jake's is a chef-driven American restaurant with three Kansas City-area locations. The site has one job: get a guest to a table or a pickup order fast.",
    ["Pickup ordering and delivery links", "Reservations by location", "Menus and happy hour", "Daily hours for each location", "Gift cards, careers and email signup"])
add("brous-law", "Brous Law", "business", "https://brouslaw.com/", "Midwest and Washington, D.C.", "Static site on Netlify",
    "Brous Law is a boutique law firm based in the Midwest and Washington, D.C.",
    [])

# ---- Podcasts and video (names from Tim, Nov 23; details to confirm)
SHOWS = [
    ("black-in-the-middle", "Black in the Middle", "Podcast", "Kansas City, Missouri",
     "Black in the Middle is a podcast by three Black friends who grew up in the suburbs. Travis Brown, Herman Watson and Tim McCoy talk through how nature and nurture shaped them, and how to handle cultural bias and differing points of view. Yoodle has produced the show since 2020.",
     ["More than 120 episodes", "Audio on all major podcast apps", "Video episodes on YouTube", "Social clips on Instagram"],
     [("Listen to the show", "https://pod.co/black-in-the-middle"), ("Watch on YouTube", "https://www.youtube.com/@blackinthemiddle"), ("Instagram", "https://www.instagram.com/_blackinthemiddle/")]),
    ("the-big-break", "The Big Break", "Podcast", "American Jazz Museum, Kansas City",
     "The Big Break is the American Jazz Museum's podcast. Host Dr. Dina Bennett, ethnomusicologist and the museum's executive director, explores jazz history through the stories behind the art: the artists, entrepreneurs and enthusiasts who made it.",
     ["Seven episodes", "Hosted by Dr. Dina Bennett", "Created by the American Jazz Museum"],
     [("Listen to the show", "https://pod.co/the-big-break")]),
    ("encourage-to-talk", "Encourage to Talk", "Podcast", "Fore the Kids Foundation",
     "Encourage to Talk is a podcast from the Fore the Kids Foundation: adult conversations around youth mental health. Host Haley Prophet talks with parents, advocates and professionals about their experiences and the resources that help.",
     ["Five episodes", "Hosted by Haley Prophet", "Created by the Fore the Kids Foundation"],
     [("Listen to the show", "https://pod.co/encourage-to-talk")]),
]
for slug, name, kind, place, about, feats, links in SHOWS:
    add(slug, name, "content", "", place, "", about, feats, kind)
    P[-1]["links"] = links
# Earlier work from the previous yoodle.com (assets come from the site backup)
ARCHIVE = ["KC Rising", "Together KC", "KC Global Design", "KC Parks", "THPRD", "Kansas City International Airport",
           "Fort Hays State University", "Lamar State College Port Arthur", "Hostos Community College", "KU Endowment",
           "Cape Cod Community College", "Unified Government of Wyandotte County", "Epiq", "The Netherland", "The Raphael Hotel",
           "Chaz on the Plaza", "Cliff's Taphouse", "Parisi Coffee", "Barrio", "Gordon Parks Elementary", "JWR Architecture",
           "Independence Square", "Scopifi", "Comp-Con", "Argyle", "Jaudon", "IIAO"]

CLIENTS = ["Nevada State University", "UT Austin Extended Campus", "Florida State University Career Center", "Kansas Judicial Branch",
           "Multistate Tax Commission", "NeighborWorks America", "KC Streetcar", "Port KC", "UMKC", "KU Endowment",
           "San Bernardino Community College District", "MiraCosta College", "Palm Beach State College", "Variety KC",
           "MARC Head Start", "American Jazz Museum"]

SERVICES = {
 "brand": dict(name="Brand", verdict="Defined.", title="Brand Strategy and Identity for Colleges and Agencies",
   desc="Brand strategy, naming, identity systems and brand standards from Yoodle. Built so the people who run your brand every day can actually use it.",
   lede="A brand is finished when your own team can use it without calling us. We get it there.",
   body=["Most brand projects end with a PDF nobody opens. Ours end with a system your staff can run: a clear position, a name and voice that hold up in a board room, an identity that works on a phone, and standards short enough to follow.",
         "We have done this for public colleges, city and regional agencies, national nonprofits and owner-run businesses since 2007. The method is the same each time. We scope it, we build it, and we hand it over working."],
   items=[("Positioning and messaging", "Who you serve, what you promise and how you say it, in language your staff will repeat."),
          ("Naming and identity", "Names, logos, color and type built for screens first, then print."),
          ("Brand standards", "A short guide and working templates, so the brand survives staff turnover."),
          ("Campaign creative", "Enrollment, awareness and fundraising campaigns that look like one organization made them.")],
   faq=[("What does a brand project include?", "Positioning, messaging, identity design and brand standards, plus the templates your team uses most. We scope each project to what you need and name a fixed outcome before we start."),
        ("Do you work with public institutions?", "Yes. Since 2007 Yoodle has worked with public colleges and universities, government agencies and nonprofits, including procurement by RFP and as a subcontractor to a prime.")]),
 "interactive": dict(name="Interactive", verdict="Launched.", title="Web Design for Higher Education and Government",
   desc="Website strategy, design, development and accessibility from Yoodle. WordPress, Drupal, Modern Campus or static: we work on the platform you have.",
   lede="Websites for organizations that answer to the public. Designed, built, tested and launched.",
   body=["A college, court or agency website is a public service. People arrive with a task: apply, register, pay, file, find a person. We design around those tasks, build on the platform your team can maintain, and test every page for speed and accessibility before it goes live.",
         "We are platform agnostic. Our live work runs on WordPress, Drupal, Modern Campus CMS and plain static HTML. We will tell you plainly when your platform is the problem and when it is not."],
   items=[("Strategy and information architecture", "Audience paths, navigation and content models based on what visitors come to do."),
          ("Design and development", "Fast, lean builds with no page-builder bloat, on your CMS or ours."),
          ("Accessibility", "WCAG 2.1 AA audits, fixes in the site's own code, retests and conformance reports."),
          ("Support and hosting", "Updates, monitoring and a person who answers when something breaks.")],
   faq=[("Which platforms does Yoodle build on?", "WordPress, Drupal, Modern Campus CMS (OmniUpdate) and static sites. We work on the platform you already have, and recommend a change only when it will save you money or risk."),
        ("Do you make websites ADA compliant?", "Yes. We audit against WCAG 2.1 Level AA, fix the issues in the site's own code and content, retest, and deliver a conformance report. We do not use overlays or widgets."),
        ("Can you work under a prime contractor?", "Yes. We regularly deliver design, development and accessibility work as a teaming partner or subcontractor.")]),
 "growth": dict(name="Growth", verdict="Measured.", title="SEO, AI Search Optimization and Paid Media",
   desc="SEO, AI search visibility, paid media and analytics from Yoodle. One integrated system across paid, organic and content, measured against the number you report.",
   lede="Found by people and by AI. Paid, organic and content run as one system and measured against one number.",
   body=["Search changed. People now ask an AI assistant as often as they type a query, and the answer names a few sources. We build your pages, data and reputation so you are one of them, and so you still rank in classic search.",
         "Then we connect it to paid media and content, and report against the number your leadership cares about: applications, enrollments, leads, bookings or donations."],
   items=[("SEO and AI search", "Technical fixes, structured data, and content written to be cited by AI answers and ranked by search engines."),
          ("Paid media", "Search and social campaigns tracked to the result, with creative tested against your competitors."),
          ("Analytics and dashboards", "One dashboard your team reads in a minute, built on your own accounts."),
          ("Local visibility", "Listings, reviews and location pages for multi-location organizations.")],
   faq=[("What is AI search optimization?", "It is the work of making your organization a source that AI assistants cite: clear facts on your pages, structured data, consistent listings and content that answers real questions directly."),
        ("How do you report results?", "Against one agreed number, such as applications, leads or bookings, in a dashboard built on accounts you own.")]),
 "content": dict(name="Content", verdict="Published.", title="Podcast, Video and Content Production",
   desc="Podcast production, video, writing and content systems from Yoodle. Planned, produced and published on a schedule your team can keep.",
   lede="Podcasts, video and writing that people finish. Planned, produced and published on schedule.",
   body=["Anyone can produce content now. Fewer organizations can produce content that is accurate, on brand and worth someone's time. We plan the series, produce the episodes and pieces, and build the publishing routine so it keeps going after launch.",
         "We have produced podcasts for museums, nonprofits and our own studio, and video and web content for colleges."],
   items=[("Podcast production", "Format, recording, editing, artwork and distribution."),
          ("Video", "Program, recruitment and story videos, cut for the website and for social."),
          ("Writing and page building", "Web copy, articles and landing pages, built straight into your CMS."),
          ("Content systems", "Calendars, templates and review steps so a person signs off on everything that ships.")],
   faq=[("Does Yoodle produce podcasts for clients?", "Yes. We handle format development, recording, editing, artwork and distribution, and can train your team to run the show."),
        ("Do you use AI to create content?", "We use AI for speed in research, drafts and editing. A person checks and approves everything before it is published under your name.")]),
}

# ---- Río Hondo College case study (source: "Rio Hondo - Yoodle Deliverable Links" and the two page lists, 2024)
RH_NEW = ["Accounting, Tax & Payroll", "Administration", "Administration of Justice, Policing & Corrections", "Alternative Energy Technology", "American Sign Language & Deaf Studies", "Animation, Games & Entertainment Art", "Anthropology", "Architectural Design, Drawing & Theory", "Areas of Study", "Art History", "Automotive Technology", "Business", "Carpentry", "Chemistry", "Child Development", "Communication Studies", "Computer Science", "Construction Engineering Management", "Creative Writing", "Dance", "Economics", "Education", "English", "English as a Second Language", "Environmental Science & Technology", "Fire Technology & Emergency Response", "General Studies", "Graphic Art & Design", "Health Science & Career Preparation", "History", "Home", "Hospitality Management", "Kinesiology, Fitness & Sports", "Mass Communications, Media & Journalism", "Mathematics", "Music", "Nursing", "Nutrition & Dietetics", "Pathway to Law School", "Philosophy", "Photography", "Physics", "Police Department", "Political Science", "Psychology", "Social Work & Services", "Sociology", "Spanish", "Studio Arts", "Welding Technology"]
RH_OPT = ["About", "Academic Calendar", "Academics", "Admissions & Records Office", "Admissions FAQ", "Adult Re-Entry Program", "Career & Technical Education", "Class Registration", "Continuing Education & Noncredit Division", "Counseling Center", "Disabled Students Program & Services", "Dreamers' Resource Center", "EMT Program", "Financial Aid", "Fire Technology Academy Programs", "International Students", "Library", "Police Academy", "Rio Promise", "Steps for First-Time College Students", "Steps for Transfer Students From Another College", "Student Life & Leadership", "Transfer Center", "Tutoring", "Veterans Service Center", "Virtual Welcome Center"]
RH_VIDEO = ["Brand video", "Campus tour", "Tutoring", "Tesla program", "Pathway to Law", "Music program", "Fire and EMT", "Child Development", "Ceramics", "Automotive program"]
RH = dict(
  lede="Río Hondo College brought Yoodle in for one engagement with nine goals: measure the website, test it with real users, set the rules for running it, then write, build and film the content that fills it.",
  stats=[("77", "existing pages rewritten and optimized"), ("50", "new pages written and built"), ("33", "area-of-study pages revised in a second round"), ("10", "video series, plus photography")],
  goals=[("Analytics and goals", "Goal setting and Google Analytics, so the college agreed on what the website is for before changing it."),
         ("Looker dashboards", "Dashboards the web team reads without an analyst, with a user guide and a plain-language glossary."),
         ("Usability testing", "Card sorting, tree testing and a first-reaction survey, turned into navigation and content recommendations."),
         ("Governance", "A web content governance guide and RACI chart, delivered with a recorded consultation."),
         ("Content journeys", "Model content journeys for the pages that matter most to students choosing a program."),
         ("Writing for the web workshop", "A recorded workshop and guide, so college staff can keep writing pages to the same standard."),
         ("Page writing, accessibility and migration", "Pages written and optimized, ADA compliance testing, and content migrated from the client's final list. Pages completed May 13, 2024. Migration completed July 26, 2024."),
         ("Media for the web", "Video series, a campus tour, a brand video and photography, shot for use on the pages we built."),
         ("Support programs finder", "A filter and sort tool for student support programs, built and deployed into the college's WordPress codebase.")])
for _p in P:
    if _p["slug"] == "rio-hondo-college":
        _p["case"] = RH
        _p["links"] = [("Watch the Río Hondo College reel", "https://vimeo.com/1230352325"), ("Visit riohondo.edu", "https://www.riohondo.edu/")]
        _p["about"] = "Río Hondo College in Whittier, California: 77 pages optimized, 50 new pages built, analytics, usability testing, governance and 10 video series by Yoodle."
