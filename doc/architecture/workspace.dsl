workspace {

    model {
        plannerUser = person "User"
        emailServerSystem = softwareSystem "Email Server" "External" "External"
        slowhopWebsite = softwareSystem "Slowhop.com" "External" "External"
        vacationPlannerSystem = softwareSystem "Vacation Planner System" "Planning vacation for group of friends" "Vacation Planner System" {
            nginx = container "Nginx" "Webserver" {
                plannerUser -> this "Uses"
            }

            core = container "Vacation Planner Core" "Django" {

                nginx -> this "Passes requests to / gets responses from"

                events = component "Events" "Create new vacation events, add users to them and vote on dates and places"
                friends = component "Friends" "Organise users in groups of friends" {
                    events -> this "Events created for group of friends"
                }

                places = component "Places" "Add and manage places to propose for users events" {
                    events -> this "Places are proposed in events"

                }
                chat = component "Chat" "Chat for users of friends groups and events" {
                    friends -> this "Uses"
                    events -> this "Uses"
                }
                users = component "Users" "User Management" {
                    friends -> this "Group users"
                }

                coreEmails = component "Email service" {
                    events -> this "Uses to notify"
                    users -> this "Uses to change password"
                }

                front = component "Frontend" "Frontend based on Django templates" {
                    users -> this "Uses"
                    friends -> this "Uses"
                    places -> this "Uses"
                    events -> this "Uses"
                    chat -> this "Uses"
                    plannerUser -> this "Uses"
                }
                placesAPI = component "Places API" "Endpoint to get current scrapping task status" {
                    front -> this "Request data"
                }

                coreEmails -> emailServerSystem "Uses"

            }
            coreDB = container "PostgreSQL" {
                core -> this "Uses as a DB"
            }

            celeryWorker = container "Celery Worker"
            redis = container "Redis"
            rabbitMQ = container "RabbitMQ"
            standaloneChrome = container "Selenium-Standalone Chrome" "Browser container for scrapper"

            scrapper = container "Web Scrapper" "Django Rest Framework" {
                core -> this "Initiates new scrappings and retrieves results"
                places -> this "Start new scrapping jobs and retrieve results"
                placesAPI -> this "Get current task status"

                webscrapper = component "Webscrapper Django App" {
                }

                restFramework = component "Django Rest Framework" {
                    webscrapper -> this "Uses"
                }

                celery = component "Celery" {
                    webscrapper -> this "Uses"
                }

                selenium = component "Selenium" {
                    webscrapper -> this "Uses"
                }

                celery -> rabbitMQ "Uses as a message broker"
                celery -> celeryWorker "Start tasks"
                celery -> redis "Uses as a task result storage"
                selenium -> standaloneChrome "Uses as a remote webdriver"
            }

            standaloneChrome -> slowhopWebsite "Scrapps website"
            coreEmails -> emailServerSystem "Uses"
        }

        plannerUser -> vacationPlannerSystem "Joins group, creates events, adds and votes on proposals to select perferct joint vacation"
        vacationPlannerSystem -> emailServerSystem "triggers email sending to users"
        vacationPlannerSystem -> slowhopWebsite "scrapps website to find suiting vacation places"
        emailServerSystem -> plannerUser "sends emails to users"
    }

    views {
        systemContext vacationPlannerSystem "SystemContext" {
            include *
            autoLayout
        }

        container vacationPlannerSystem "Container" {
            include *
            autoLayout
        }

        component core {
            include *
            autoLayout
        }

        component scrapper {
            include *
            autoLayout
        }

        styles {
            element "External" {
                background #808080
                shape RoundedBox
            }
        }
        theme default

    }

}
