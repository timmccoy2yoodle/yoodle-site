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
    "Crowder College is a community college in southwest Missouri with a plain promise on its homepage: changing lives and strengthening communities, one student at a time. Yoodle designed and built the new crowder.edu on WordPress, and it launched in 2026.",
    ["Paths for prospective students, faculty and staff, parents and family, and alumni", "Program finder", "Events and news", "Course schedule and catalog links", "Foundation and giving"])
add("palm-beach-state-college", "Palm Beach State College", "higher-ed", "https://pbsc.edu/", "Palm Beach County, Florida", "",
    "Palm Beach State College opens with \"A Smart Start\" and walks new students from first question to first class.",
    ["Where to Start guide", "Career Pathways with pathway maps", "Important dates", "Featured news and upcoming events", "Student success spotlights"])
add("miracosta-college", "MiraCosta College", "higher-ed", "https://miracosta.edu/", "Oceanside, California", "Modern Campus CMS (OmniUpdate)",
    "MiraCosta College serves coastal North San Diego County from campuses in Oceanside and Cardiff, and a technology career institute in Carlsbad.",
    ["Paths for new, returning, international, high school and noncredit students", "Program finder and Career Coach", "Site search", "Virtual campus tours", "News and events"])
add("missouri-western-state-university", "Missouri Western State University", "higher-ed", "https://www.missouriwestern.edu/", "St. Joseph, Missouri", "",
    "Everyone already called it MoWest. Students, alumni and the community had used the name for years. The university's own graphic standards said otherwise: the brand was Missouri Western, and \"Mo. West\" sat on the list of unacceptable forms. Yoodle made the case to stop correcting people and claim the name. Missouri Western State University chose Yoodle through public RFP 24-049 for market research and brand development, and the work grew into a rebrand, a new logo, a marketing campaign and advertising.",
    ["Research and discovery: on-site stakeholder sessions, group interviews with alumni, students, prospective students, faculty, staff and community leaders, a brand collateral inventory, a SWOT analysis and personas", "Brand positioning workshop and message matrices for three recruitment audiences", "Brand strategy", "Communication audit and creative concept", "The MoWest logo: a primary mark, a stacked mark and secondary MW and MoWest marks, approved by the university in November 2024", "\"More at MoWest\" campaign creative for outdoor and social", "Campaign and marketing plan", "Brand launch video, 2025", "Ongoing marketing support on retainer, 2024 to 2025"], "Brand and marketing")
P[-1]["quote"] = ("We\u2019re good to go. President Kennedy loved everything!", "Tama Wagner, Chief Assistant for Strategic Initiatives, Office of the President, Missouri Western State University")
P[-1]["gallery"] = [("The primary MoWest logo, in black and in white", 1448, 807), ("The stacked MoWest logo", 1448, 807), ("Secondary marks: MW with the griffon, W MoWest and MoWest", 1448, 807), ("More at MoWest campaign banners", 1448, 807), ("More at MoWest social posts", 1448, 807)]
add("yoodle-education-services", "Yoodle Education Services with UMKC", "higher-ed", "", "Kansas City, Missouri", "",
    "Yoodle Education Services (YES) is the workforce school Yoodle built. With the UMKC School of Computing and Engineering as university partner and the Full Employment Council of Kansas City as workforce partner, Yoodle's people taught 16-week courses that give working adults debt-free training for technology jobs.",
    ["Web developer fundamentals: HTML, CSS, JavaScript and WordPress, with a nonprofit website built as the class project", "Digital marketing: design thinking, brand strategy, content, SEO, social media and analytics", "Full-stack courses in MongoDB, Express, Angular and Node, and in ASP.NET Core", "A four-week IT support course", "Curriculum written and taught by Yoodle's designers, developers and strategists", "The Let's Skill Up brand, info sessions, flyers and advertising that filled each cohort", "Enrollment and funding through the Full Employment Council and KansasWorks"], "Workforce training")
P[-1]["quote"] = ("Our partnership with The Full Employment Council and Yoodle has allowed UMKC\u2019s School of Computing and Engineering to bring timely and much-needed web development training to Kansas City.", "Christina Davis, Director of Continuing Education, UMKC School of Computing and Engineering")
P[-1]["gallery"] = [("Let's Skill Up brand mood board", 1600, 916), ("Let's Skill Up brand concept", 1600, 1018)]
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
 "brand": dict(name="Brand", verdict="Find your voice.", title="Brand Strategy and Identity for Colleges and Agencies",
   desc="Brand strategy, naming, identity systems and brand standards from Yoodle. Built so the people who run your brand every day can actually use it.",
   lede="Give people a reason to care, and give your own team a brand they can carry without calling us.",
   body=["Most brand projects end with a PDF nobody opens. Ours end with a system your staff can run: a clear position, a name and voice that hold up in a board room, an identity that works on a phone, and standards short enough to follow.",
         "We have done this for public colleges, city and regional agencies, national nonprofits and owner-run businesses since 2007. The method is the same each time. We scope it, we build it, and we hand it over working."],
   items=[("Positioning and messaging", "Who you serve, what you promise and how you say it, in language your staff will repeat."),
          ("Naming and identity", "Names, logos, color and type built for screens first, then print."),
          ("Brand standards", "A short guide and working templates, so the brand survives staff turnover."),
          ("Campaign creative", "Enrollment, awareness and fundraising campaigns that look like one organization made them.")],
   faq=[("What does a brand project include?", "Positioning, messaging, identity design and brand standards, plus the templates your team uses most. We scope each project to what you need and name a fixed outcome before we start."),
        ("Do you work with public institutions?", "Yes. Since 2007 Yoodle has worked with public colleges and universities, government agencies and nonprofits, including procurement by RFP and as a subcontractor to a prime.")]),
 "technology": dict(name="Technology", verdict="Make every interaction work harder.", title="Web Design for Higher Education and Government",
   desc="Website strategy, design, development and accessibility from Yoodle. WordPress, Drupal, Modern Campus or static: we work on the platform you have.",
   lede="Websites, applications and digital experiences designed around the people who use them, and built to work for every one of them.",
   body=["A college, court or agency website is a public service. People arrive with a task: apply, register, pay, file, find a person. We design around those tasks, build on the platform your team can maintain, and test every page for speed and accessibility before it goes live.",
         "We are platform agnostic. Our live work runs on WordPress, Drupal, Modern Campus CMS and plain static HTML. We will tell you plainly when your platform is the problem and when it is not."],
   items=[("Strategy and information architecture", "Audience paths, navigation and content models based on what visitors come to do."),
          ("Design and development", "Fast, lean builds with no page-builder bloat, on your CMS or ours."),
          ("Accessibility", "WCAG 2.1 AA audits, fixes in the site's own code, retests and conformance reports."),
          ("Support and hosting", "Updates, monitoring and a person who answers when something breaks.")],
   faq=[("Which platforms does Yoodle build on?", "WordPress, Drupal, Modern Campus CMS (OmniUpdate) and static sites. We work on the platform you already have, and recommend a change only when it will save you money or risk."),
        ("Do you make websites ADA compliant?", "Yes. We audit against WCAG 2.1 Level AA, fix the issues in the site's own code and content, retest, and deliver a conformance report. We do not use overlays or widgets."),
        ("Can you work under a prime contractor?", "Yes. We regularly deliver design, development and accessibility work as a teaming partner or subcontractor.")]),
 "growth": dict(name="Growth", verdict="Attention, turned into momentum.", title="SEO, AI Search Optimization and Paid Media",
   desc="SEO, AI search visibility, paid media and analytics from Yoodle. One integrated system across paid, organic and content, measured against the number you report.",
   lede="Found wherever people look. Paid, organic and content run as one system and measured against one number.",
   body=["Search changed. People now ask an AI assistant as often as they type a query, and the answer names a few sources. We build your pages, data and reputation so you are one of them, and so you still rank in classic search.",
         "Then we connect it to paid media and content, and report against the number your leadership cares about: applications, enrollments, leads, bookings or donations."],
   items=[("SEO and AI search", "Technical fixes, structured data, and content written to be cited by AI answers and ranked by search engines."),
          ("Paid media", "Search and social campaigns tracked to the result, with creative tested against your competitors."),
          ("Analytics and dashboards", "One dashboard your team reads in a minute, built on your own accounts."),
          ("Local visibility", "Listings, reviews and location pages for multi-location organizations.")],
   faq=[("What is AI search optimization?", "It is the work of making your organization a source that AI assistants cite: clear facts on your pages, structured data, consistent listings and content that answers real questions directly."),
        ("How do you report results?", "Against one agreed number, such as applications, leads or bookings, in a dashboard built on accounts you own.")]),
 "content": dict(name="Content", verdict="Stories people finish.", title="Podcast, Video and Content Production",
   desc="Podcast production, video, writing and content systems from Yoodle. Planned, produced and published on a schedule your team can keep.",
   lede="Storytelling people finish, across every place your brand speaks. Planned, produced and published on schedule.",
   body=["A content experience is everything someone reads, watches, hears and clicks on the way to trusting you. Most organizations produce those pieces in separate rooms: the website here, social there, the course catalog somewhere else. We treat them as one story and make each piece lead to the next.",
         "That takes storytelling and it takes systems. We find the story, produce it in the formats your audience actually uses, and build the routine that keeps it publishing after launch."],
   items=[("Website content", "Page writing, restructuring and migration, built straight into your CMS."),
          ("Editorial", "Articles, features and newsletters with a point of view and a schedule."),
          ("Social media", "Short-form video, graphics and captions made for each platform, not resized for it."),
          ("Podcasts", "Format, recording, editing, artwork and distribution."),
          ("Video and photography", "Program, recruitment and brand stories, cut for the website and for social."),
          ("Learning content", "Courses, training modules and LMS content people can finish and use."),
          ("Content systems", "Calendars, templates and review steps so a person signs off on everything that ships.")],
   faq=[("Does Yoodle produce podcasts for clients?", "Yes. We handle format development, recording, editing, artwork and distribution, and can train your team to run the show."),
        ("Do you use AI to create content?", "We use AI for speed in research, drafts and editing. A person checks and approves everything before it is published under your name.")]),
}

# ---- Río Hondo College case study (source: "Rio Hondo - Yoodle Deliverable Links" and the two page lists, 2024)
RH_NEW = ["Accounting, Tax & Payroll", "Administration", "Administration of Justice, Policing & Corrections", "Alternative Energy Technology", "American Sign Language & Deaf Studies", "Animation, Games & Entertainment Art", "Anthropology", "Architectural Design, Drawing & Theory", "Areas of Study", "Art History", "Automotive Technology", "Business", "Carpentry", "Chemistry", "Child Development", "Communication Studies", "Computer Science", "Construction Engineering Management", "Creative Writing", "Dance", "Economics", "Education", "English", "English as a Second Language", "Environmental Science & Technology", "Fire Technology & Emergency Response", "General Studies", "Graphic Art & Design", "Health Science & Career Preparation", "History", "Home", "Hospitality Management", "Kinesiology, Fitness & Sports", "Mass Communications, Media & Journalism", "Mathematics", "Music", "Nursing", "Nutrition & Dietetics", "Pathway to Law School", "Philosophy", "Photography", "Physics", "Police Department", "Political Science", "Psychology", "Social Work & Services", "Sociology", "Spanish", "Studio Arts", "Welding Technology"]
RH_OPT = ['About', 'Academic Calendar', 'Academics', 'AccessRio Tutorials', 'Administration of Justice & Fire Technology Division', 'Admissions & Records Office', 'Admissions FAQ', 'Adult Re-Entry Program', 'Automotive Technology', 'Automotive Technology Bachelor of Science', 'Business Division', 'Career & Technical Education', 'Center for Career & Re-Entry Services', 'Child Care', 'Child Development Center', 'Class Registration', 'Clubs & Organizations', 'Commencement', 'Computer Information Technology', 'Contact the South Whittier Educational Center', 'Continuing Education & Noncredit Division', 'Continuing Education for First-Time College Students', 'Continuing Education for Returning Students', 'Counseling Center', 'Disabled Students Program & Services', 'Disbursements', 'Division of Arts & Cultural Programs', 'Division of Behavioral and Social Sciences', 'Division of Communications & Languages', 'Division of Health Science & Nursing', 'Division Of Kinesiology, Dance & Athletics', 'Division of Mathematics, Sciences & Engineering', "Dreamers' Resource Center", 'El Monte Educational Center', 'EMT Program', 'Enrichment Students', 'EOP&S/CARE/NextUp', 'Finance & Business Division', 'Financial Aid', 'Fire Technology Academy Programs', 'Generic Associate Degree Nursing Program', 'Important Dates & Deadlines', 'International Students', 'Library', 'Locations', 'LVN-Associate Degree Nursing Program', 'Marketing & Communications Department', 'New Police Academy Cadets', 'New Wildland Fire Academy Cadets', 'Office of Distance Education', 'Office of Human Resources', 'Pathway to Law School', 'Photography', 'Police Academy', "Police Academy Sessions - (Recommend removing this page if the Extended Academy Session doesn't return)", 'Río Hondo College Educational Center at Pico Rivera', 'Rio Hondo College Foundation', 'Rio Promise', 'RioSource', 'RioSource Room Food Pantry', 'Steps for Dual Enrollment K-12 & Adult Education', 'Steps for First-Time College Students', 'Steps for Returning Río Hondo College Students', 'Steps for Transfer Students From Another College', 'Student Forms', 'Student Health & Psychological Services', 'Student Life & Leadership', 'Student Success Center', 'Summer Bridge Program', 'Transcripts', 'Transfer Center', 'Transfer Planning & General Education Patterns', 'Tutoring', 'Veterans Service Center', 'Virtual Welcome Center', 'Vision, Mission & Values', 'Ways to Give']
RH_REV = ['Accounting, Tax & Payroll', 'Administration of Justice, Policing & Corrections', 'Alternative Energy Technology', 'Animation, Games & Entertainment Art', 'Architectural Design, Drawing & Theory', 'Areas of Study', 'Art History', 'Automotive Technology', 'Business', 'Communication Studies', 'Computer Science', 'Economics', 'English', 'Environmental Science & Technology', 'Fire Technology & Emergency Response', 'Graphic Art & Design', 'Health Science & Career Preparation', 'History', 'Hospitality Management', 'Kinesiology & Athletics', 'Mass Communications, Media & Journalism', 'Mathematics', 'Music & Integrated Technology', 'Nursing', 'Nutrition & Dietetics', 'Photography', 'Physics', 'Political Science', 'Psychology', 'Sociology', 'Spanish', 'Studio Arts', 'Welding Technology']
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

# ---- Live-site numbers, read from each client's Google Analytics (GA4) property
GA_RANGE = "Google Analytics, November 24, 2025 to November 23, 2026"
for _slug, _stats in {
    "palm-beach-state-college": [("910K", "active users in twelve months"), ("3.3M", "page views"), ("2M", "visits"), ("797K", "visits from organic search")],
    "nevada-state-university": [("921K", "active users in twelve months"), ("2.5M", "page views"), ("1.5M", "visits"), ("2.5K", "leads from request-info forms")],
}.items():
    for _p in P:
        if _p["slug"] == _slug: _p["stats"] = _stats

# ---- What each service covers, in the words buyers and search engines use
for _k, _kw in {
    "brand": "Brand strategy, market research, positioning and messaging, naming, logo development, graphic design, visual identity, brand standards, rebrands and storytelling.",
    "technology": "Website design and development, UX and wireframes, WordPress, Drupal and Modern Campus, ADA and WCAG 2.1 AA compliance, accessibility audits, content migration, web apps, dashboards, hosting and support.",
    "growth": "SEO, AI search optimization (AEO and GEO), local SEO, Google Ads and paid social, enrollment and lead generation campaigns, email marketing, analytics and reporting, conversion optimization and fractional CMO leadership.",
    "content": "Content strategy, copywriting, podcast production, video production, photography, social media content, blogs and email newsletters.",
}.items(): SERVICES[_k]["kw"] = _kw

# ---- Three practices, each with named capabilities and a plain definition. Names, taglines and sub-lines are Tim's (Nov 25 2026)
PILLARS = [
 dict(key='brand', name='Brand', lede='Find your voice. Give people a reason to care.', sub='Strategy / Identity / Messaging',
      links=[('/services/brand/', 'More on brand.')], caps=[
  ('Research & Insight', 'Surveys, interviews and perception studies that replace opinion with evidence before anything gets designed.'),
  ('Brand Strategy & Positioning', 'Who you are, who you serve and why it matters, plus how your programs, departments and locations sit under one name.'),
  ('Naming, Voice & Messaging', 'Names, taglines, voice and key messages your people will actually use.'),
  ('Logo & Visual Identity', 'Logo, color, type and imagery, with the rules that keep them consistent in every hand.'),
  ('Brand Standards & Templates', 'Templates, asset libraries and guidelines built so your team can produce on-brand work without calling us.'),
  ('Brand for Search & Assistants', 'Shaping how search engines and AI assistants describe you, so the answer matches the brand.'),
  ('Launches & Live Events', "Launches, anniversaries and events that put the brand in a room with the people it's for."),
 ]),
 dict(key='technology', name='Technology', lede='Make every interaction work harder.', sub='Websites / Accessibility / Digital experiences',
      links=[('/services/technology/', 'More on technology.')], caps=[
  ('Digital Strategy & Planning', 'Which digital investments come first, which can wait, and which you can skip.'),
  ('Content Experience Design', 'The whole journey mapped across site, search, email and people, so each step leads to the next.'),
  ('UX Strategy & Information Architecture', 'Sitemaps, user journeys and navigation that match how people actually look for things.'),
  ('Web Design & Development', 'Designed and built by hand on the platform that suits you, or the one you already own.'),
  ('Accessibility & User Testing', 'WCAG 2.1 AA audits, fixes and certification, plus card sorts, tree tests and sessions with real users.'),
  ('Custom Applications & Dashboards', 'Internal tools, portals and reporting built for the way your organization really works.'),
  ('Learning Platforms', 'Course sites and training systems for students, staff and customers.'),
  ('Online Stores & Checkout', 'Stores and checkout flows that make buying simple.'),
  ('Component Libraries & Front-End Systems', 'Reusable components that keep design and code in step as the product grows.'),
  ('Prototyping', 'A working version in days, so you can react to something real before committing the budget.'),
  ('AI Integration & Automation', 'Assistants, automations and smarter search built into the tools your team and customers already use.'),
  ('Hosting, Integrations & Support', 'Launch, connect it to the systems around it, and keep it secure and current.'),
 ]),
 dict(key='marketing', name='Marketing', lede='Turn attention into meaningful momentum.', sub='Campaigns / Content / Growth',
      links=[('/services/growth/', 'More on growth.'), ('/services/content/', 'More on content.')], caps=[
  ('Marketing Strategy & Planning', 'One plan across paid, organic and content, tied to a number your leadership already watches.'),
  ('Audience Personas & Journeys', 'Your audiences sorted by what each needs to hear, and the path each one takes to a decision.'),
  ('Campaigns & Advertising', 'A single idea carried across outdoor, digital, social and print.'),
  ('Enrollment & Lead Generation', 'Lead generation and enrollment campaigns built around the next step you need someone to take.'),
  ('Paid Media', 'Google, Meta and social advertising, planned, placed and reported against cost per result.'),
  ('SEO & AI Search', 'Technical fixes, structured data and content written to rank in search and be cited in AI answers.'),
  ('Podcast, Video & Editorial Production', 'Podcasts, video, photography, editorial and web copy, produced end to end.'),
  ('Social Media Management', 'Day-to-day publishing and conversation in the places your audience already spends time.'),
  ('Analytics & Reporting', "Dashboards that show what's working in plain language, and what we'd change next."),
  ('Fractional CMO', 'A senior marketing leader inside your organization, with our team behind them.'),
 ]),
]

# ---- Engagement facts read from signed agreements, proposals and statements of work in the client folders (Nov 26 2026).
# (when, scope). A project with an entry here shows these and drops the scope CONFIRM tag.
ENG = {
 "nevada-state-university": ("2022 to present", "Yoodle won the university's public RFP for website redesign and maintenance in 2022. The redesign was followed by statements of work for a program finder, a policies library, a staff directory and a content migration in 2023, and a hosting and support plan from 2024."),
 "san-bernardino-community-college-district": ("Contract signed July 2020", "A ten-month redesign: sitemap, wireframes, three creative concepts, layouts for ten main templates, accessible front-end code, implementation in the district's Omni CMS, content migration and an ADA compliance report. A later statement of work covered website modifications."),
 "compton-college": ("Proposal February 2022", "A ten-month redesign: sitemap, wireframes, three creative concepts, layouts for the main templates, accessible front-end code built for Modern Campus Omni CMS, user acceptance testing, an ADA compliance report and search engine optimization at rollout."),
 "ut-austin-extended-campus": ("2021 to 2023", "A six-month build for the university's professional education gateway: sitemap, wireframes, two creative concepts, layouts for ten main templates, accessible front-end code and implementation in Drupal on the university's own Drupal Kit, with an ADA compliance report and search engine optimization at rollout."),
 "earth-center": ("2024 to present", "Yoodle won the public RFP run by Central Carolina Community College in 2024 and kicked off that April. Website maintenance agreements followed in December 2024 and June 2025."),
 "crowder-college": ("Contract signed October 2023, launched 2026", "Discovery with stakeholder and user interviews and an online survey, a new sitemap and navigation, wireframes and two creative concepts, six page templates coded to Section 508 and tested for ADA compliance, a WordPress build, migration of the top 100 pages, analytics, SEO guidance, editor training with a written manual, launch and post-launch support."),
 "swift-education-center": ("2022 to present", "Yoodle rebuilt and redesigned the SWIFT Education Center website under an agreement with the University of Kansas in 2022. A second agreement followed in 2023, and a WCAG 2.1 AA accessibility audit and certification in 2026."),
 "missouri-kinship-navigator": ("2024", "A website build for the University of Missouri under a professional services agreement, followed by hosting and maintenance."),
 "kansas-judicial-branch": ("Contract signed May 2018", "A website development agreement with the Office of Judicial Administration, with a statement of work covering design and build."),
 "multistate-tax-commission": ("2021 to present", "Yoodle moved the commission's website from Kentico to WordPress and brought it live in 2023, then kept it running under maintenance and support agreements from 2023 to 2025. A website refresh was signed in October 2026."),
 "kc-streetcar": ("", "A website redesign, followed by a signed website maintenance agreement."),
 "marc-head-start": ("Contract signed July 2019", "A website design and build for the Mid-America Regional Council's Head Start program."),
 "variety-socal": ("Contract signed December 2019", "A website and marketing engagement: design, build and the marketing to launch it."),
 "variety-kc": ("Client since 2017", "Website, brand and marketing work for the chapter since 2017, including signage for its inclusive spaces."),
 "wentworth-financial-communications": ("Contract signed October 2018", "Website design and development."),
 "dr-amy-k-patel": ("2020", "A brand-building engagement in early 2020, a website design and build that summer, and a maintenance agreement from December 2020."),
}
for _p in P:
    if _p["slug"] in ENG: _p["eng"] = ENG[_p["slug"]]

for _p in P:
    if _p["slug"] == "missouri-western-state-university": _p["eng"] = ("2024 to 2025", "")
    if _p["slug"] == "yoodle-education-services":
        _p["eng"] = ("2020 to 2025", "")
        _p["stats"] = [("50", "graduates on the roster by August 2023"), ("9", "web development cohorts by late 2023"), ("5", "digital marketing cohorts by late 2023"), ("6", "graduates hired by Yoodle")]
        _p["stats_src"] = "Yoodle and UMKC graduate roster, updated August 2023, and program invoices through November 2023"
        _p["about"] += " The first course agreements were signed in October 2020 and classes began in early 2021. A new AI digital marketing course was written in 2025."

# ---- More engagement facts (client folder contents and file dates, Nov 26 2026)
ENG.update({
 "cochise-college": ("2023 to 2024", "A website redesign that kicked off in March 2023, designed and coded by Yoodle to Modern Campus Omni CMS design standards and implemented with Modern Campus."),
 "palm-beach-state-college": ("2022 to 2024", "A full website redesign run to a shared project plan with the college's web teams, from discovery in 2022 through build, testing and rollout in 2024."),
 "neighborworks-america": ("Client since 2019", "Project contracts every year from 2020 to 2022 under a main agreement, then statements of work for an ADA and Section 508 accessibility report, the move to Google Analytics 4 in 2022, application monitoring, and a testing plan in 2023."),
 "savvy-bridal": ("2026", "Yoodle rebuilt savvybridalboutique.com from the ground up as a static site in 2026."),
})
YEARS_ARCHIVE = {"cape-cod-community-college": "2018", "parisi-coffee": "2019 to 2020", "cliffs-taphouse": "2021", "together-kc": "2020", "kc-rising": "2020 to 2022",
 "kc-global-design": "2020 to 2022", "the-raphael-hotel": "2019 to 2021", "chaz-on-the-plaza": "2019 to 2021", "the-netherland": "2020", "the-soul-of-santa": "2020 to present",
 "unified-government": "2020", "kansas-city-international-airport": "2019", "jaudon": "2019 to 2020", "gordon-parks-elementary": "2018 to 2019"}
for _p in P:
    if _p["slug"] in ENG: _p["eng"] = ENG[_p["slug"]]
    if _p["slug"] == "compton-college": _p["platform"] = "Modern Campus Omni CMS"

# ---- Scope and platform from Tim (Nov 26 2026)
_RD = "Website redesign and development."
ENG.update({"miracosta-college": ("", _RD), "fsu-career-center": ("", _RD), "ci3t": ("", _RD), "music-theater-heritage": ("", _RD),
 "nick-and-jakes": ("2026", "Website redesign and development. Yoodle designed and built the new site as fast static pages, with no content management system to slow it down or patch."),
 "brous-law": ("2026", "Website redesign and development. Yoodle designed and built the site as fast static pages, with no content management system to slow it down or patch.")})
_PLAT = {"ci3t": "Drupal", "fsu-career-center": "Drupal", "music-theater-heritage": "WordPress", "kansas-judicial-branch": "Kentico",
 "palm-beach-state-college": "Modern Campus Omni CMS", "neighborworks-america": "Kentico"}
for _p in P:
    if _p["slug"] in ENG: _p["eng"] = ENG[_p["slug"]]
    if _p["slug"] in _PLAT: _p["platform"] = _PLAT[_p["slug"]]

# ---- Tim, Nov 26 2026: never display a client's exact analytics numbers. Raw figures stay here for reference only;
# pages may show percentage changes between stated periods instead (key "stats", with "stats_src").
for _p in P:
    if _p.get("stats") and not _p.get("stats_src"): _p["ga_private"] = _p.pop("stats")

# ---- Nov 27 2026: growth shown as percentage change only (Tim's rule). Pulled from the client's GA4 property
# (nevadastate.edu, a9084605 p403568979). Raw: users 661,356 -> 921,150; sessions 1,246,065 -> 1,581,865;
# organic search sessions 579,157 -> 746,037; engaged sessions 550,717 -> 646,001; views 2,326,093 -> 2,521,386.
# Palm Beach State: no comparison possible. Its GA property stopped tracking the public site (now mostly portal pages).
for _p in P:
    if _p["slug"] == "nevada-state-university":
        _p["stats"] = [("+39%", "more people reached"), ("+29%", "more visits from search"), ("+27%", "more visits overall"), ("+17%", "more engaged visits")]
        _p["stats_src"] = "Google Analytics. The site's first full year, November 24, 2023 to November 23, 2024, compared with November 24, 2025 to November 23, 2026"

# ---- Nov 27 2026: service tags per project, from Tim's marked-up sheet "Yoodle related work: service tags and rankings"
# (claude.ai/artifact/UR2wgnZhiKhVsU6DygjCts). Keys match SERVICES; "growth" is Marketing. Related work on a service page
# only ever shows projects tagged for that service. SVC_TOP = Tim's ranked picks, shown first in order.
SVC_TAGS = {
    "missouri-western-state-university": ["brand", "growth"],
    "nevada-state-university": ["technology"],
    "san-bernardino-community-college-district": ["technology", "content"],
    "compton-college": ["technology", "content"],
    "rio-hondo-college": ["brand", "technology", "content"],
    "ut-austin-extended-campus": ["technology", "content"],
    "earth-center": ["technology", "content"],
    "fsu-career-center": ["technology"],
    "cochise-college": ["technology", "content"],
    "crowder-college": ["technology", "content"],
    "palm-beach-state-college": ["technology", "content"],
    "miracosta-college": ["technology"],
    "yoodle-education-services": [],
    "ci3t": ["technology"],
    "swift-education-center": ["technology", "content"],
    "missouri-kinship-navigator": ["technology"],
    "kansas-judicial-branch": ["brand", "technology"],
    "multistate-tax-commission": ["technology"],
    "neighborworks-america": ["brand", "technology"],
    "kc-streetcar": ["technology"],
    "marc-head-start": ["brand", "technology"],
    "music-theater-heritage": ["brand", "technology", "growth"],
    "variety-socal": ["technology"],
    "variety-kc": ["brand", "technology", "growth", "content"],
    "wentworth-financial-communications": ["technology", "growth"],
    "dr-amy-k-patel": ["brand", "technology", "growth"],
    "savvy-bridal": ["brand", "technology", "growth", "content"],
    "nick-and-jakes": ["brand", "technology", "growth"],
    "brous-law": ["brand", "technology", "content"],
    "black-in-the-middle": ["brand", "technology", "growth", "content"],
    "the-big-break": ["brand", "technology", "content"],
    "encourage-to-talk": ["brand", "technology", "content"],
    "the-raphael-hotel": ["brand", "growth"],
    "the-soul-of-santa": ["brand", "technology", "growth", "content"],
    "jaudon": ["brand"],
    "the-netherland": ["brand"],
    "chaz-on-the-plaza": ["brand"],
    "kc-parks": ["brand", "technology", "growth", "content"],
    "thprd": ["brand", "growth"],
    "barrio": ["brand", "growth"],
    "argyle": ["brand", "technology"],
    "gordon-parks-elementary": ["brand", "growth"],
    "scopifi": ["brand", "technology"],
    "national-comp": ["brand"],
    "independence-square": ["brand", "technology"],
    "iaao": ["brand"],
    "hostos-community-college": ["technology"],
    "cliffs-taphouse": ["brand", "technology", "growth"],
    "jwr-architecture": ["brand", "technology"],
    "ku-endowment": ["technology"],
    "parisi-coffee": ["growth"],
    "cape-cod-community-college": ["technology"],
    "together-kc": ["technology"],
    "kc-global-design": ["technology"],
    "kc-rising": ["technology"],
    "epiq-systems": ["technology"],
    "unified-government": ["technology"],
    "lamar-state-college": ["technology"],
    "fort-hays-state-university": ["technology"],
    "kansas-city-international-airport": ["technology"],
}
SVC_TOP = {"brand": ["missouri-western-state-university"]}
SVC_KIND = {"brand": "Brand and marketing", "growth": "Brand and marketing", "content": "Podcast", "technology": "Website"}
SVC_OLDER = {"music-theater-heritage", "variety-socal", "variety-kc", "dr-amy-k-patel"}  # Tim marked these Archive in the sheet
SVC_LABEL = {"brand": "Brand", "technology": "Technology", "growth": "Marketing", "content": "Content"}

# ---- Nov 27 2026: the MoWest story (Tim). Sources: the university's old Graphic Standards Manual, its July 15, 2025
# announcement and new brand guide, Yoodle's Nov 13, 2024 deck "MO West Logo + Campaign Creative Direction", and the
# RFP 24-049 award email of Dec 19, 2023. Name is spelled MoWest, as the university's brand guide requires.
for _p in P:
    if _p["slug"] == "missouri-western-state-university":
        _p["story"] = [
            "For years, the university's graphic standards manual set the rule. First reference: Missouri Western State University. Second reference: Missouri Western. \"Mo. West\" was listed as an unacceptable form in print, on apparel, on the website and on social media. The name people actually used had no official place.",
            "Missouri Western selected Yoodle in December 2023. We started by listening, in on-site sessions and group interviews with students, prospective students, alumni, faculty, staff and community leaders. In November 2024 we presented the logo and campaign direction. One section was titled \"Claiming a Nickname.\" It showed how other universities had made a nickname their primary or secondary mark, and argued that Missouri Western should do the same with the name its people already used. The university approved the direction the next day.",
            "On July 15, 2025, the university announced MoWest as the primary way it's identified, with a sharper Griffon, new primary marks and a recruitment campaign, More at MoWest. The full name stays on diplomas, transcripts and legal documents. The new brand guide reverses the old rule: MoWest comes first, and \"Missouri Western\" is now on the list of forms to avoid.",
            "We didn't invent a name. We made the case for the one the university already had."]
        _p["story_src"] = [("Graphic Standards Manual, Missouri Western State University", "https://www.missouriwestern.edu/cps/wp-content/uploads/sites/110/2018/11/GraphicStandards.pdf"),
                           ("University announcement, July 15, 2025", "https://www.missouriwestern.edu/news/2025/07/15/mowest-embraces-a-familiar-name-as-its-primary-identifier/"),
                           ("MoWest Brand Guide", "https://www.missouriwestern.edu/brand/brand-guide/")]
