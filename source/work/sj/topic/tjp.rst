taskjuggler tjp files
========================

envc
-----

::

/*
 * This file contains an example project. It is part of the
 * TaskJuggler project management tool. It uses a made up software
 * development project to demonstrate some of the basic features of
 * TaskJuggler. Please see the TaskJuggler manual for a more detailed
 * description of the various syntax elements.
 */
project feeder "智能环控器产品开发项目"  2022-09-10 +12m {
  # Set the default time zone for the project. If not specified, UTC
  # is used.
  timezone "Asia/Shanghai"
  # Hide the clock time. Only show the date.
  timeformat "%Y-%m-%d"
  # Use US format for numbers
  numberformat "-" "" "," "." 1
  # Use US financial format for currency values. Don't show cents.
  currencyformat "(" ")" "," "." 0
  # Pick a day during the project that will be reported as 'today' in
  # the project reports. If not specified, the current day will be
  # used, but this will likely be outside of the project range, so it
  # can't be seen in the reports.
  # now 2002-03-05-13:00
  # The currency for all money values is the US Dollar.
  currency "CNY"

  # We want to compare the baseline scenario to one with a slightly
  # delayed start.
  scenario plan "Plan" {
    scenario delayed "Delayed"
  }
  extend resource {
    text Phone "Phone"
  }
}

# This is not a real copyright for this file. It's just used as an example.
copyright "© Copyright 2022 SGI, ltd. All Rights Reversed"

# The daily default rate of all resources. This can be overridden for each
# resource. We specify this, so that we can do a good calculation of
# the costs of the project.
# rate 390.0

# Register Good Friday as a global holiday for all resources.
# leaves holiday "Good Friday" 2002-03-29
# flags team

# This is one way to form teams
# macro allocate_developers [
#   allocate dev1
#   allocate dev2
#   allocate dev3
# ]
# 
# # In order to do a simple profit and loss analysis of the project we
# # specify accounts. One for the development costs, one for the
# # documentation costs, and one account to credit the customer payments
# # to.
# account cost "Project Cost" {
#   account dev "Development"
#   account doc "Documentation"
# }
# account rev "Payments"
# # # The Profit&Loss analysis should be rev - cost accounts.
# # balance cost rev
# 
# resource boss "Paul Henry Bullock" {
#   email "phb@crappysoftware.com"
#   Phone "x100"
#   rate 480
# }
# resource dev "Developers" {
#   managers boss
#   resource dev1 "Paul Smith" {
#     email "paul@crappysoftware.com"
#     Phone "x362"
#     rate 350.0
#   }
#   resource dev2 "S茅bastien Bono" {
#     email "SBono@crappysoftware.com"
#     Phone "x234"
#   }
#   resource dev3 "Klaus M眉ller" {
#     email "Klaus.Mueller@crappysoftware.com"
#     Phone "x490"
#     leaves annual 2002-02-01 - 2002-02-05
#   }
#   flags team
# }
# resource misc "The Others" {
#   managers boss
#   resource test "Peter Murphy" {
#     email "murphy@crappysoftware.com"
#     Phone "x666"
#     limits { dailymax 6.4h }
#     rate 310.0
#   }
#   resource doc "Dim Sung" {
#     email "sung@crappysoftware.com"
#     Phone "x482"
#     rate 300.0
#     leaves annual 2002-03-11 - 2002-03-16
#   }
# 
#   flags team
# }

# Now we specify the work packages. The whole project is described as
# a task that contains subtasks. These subtasks are then broken down
# into smaller tasks and so on. The innermost tasks describe the real
# work and have resources allocated to them. Many attributes of tasks
# are inherited from the enclosing task. This saves you a lot of typing.
task AcSo "Accounting Software" {

#  # All work-related costs will be booked to this account unless the
#  # subtasks specify something different.
#  chargeset dev
#  # For the duration of the project we have running cost that are not
#  # included in the labor cost.
#  charge 170 perday
#  responsible boss

  task spec "Specification" {
    # The effort to finish this task is 20 man-days.
    effort 20d
    # Now we use the macro declared above to allocate the resources
    # for this task. Because they can work in parallel, they may finish this
    # task earlier than in 20 working-days.
    ${allocate_developers}
    # Each task without subtasks must have a start or an end
    # criterion and a duration. For this task we use a reference to a
    # milestone defined further below as the start criterion. So this task
    # can not start before the specified milestone has been reached.
    # References to other tasks may be relative. Each exclamation mark (!)
    # means 'in the scope of the enclosing task'. To descent into a task, the
    # fullstop (.) together with the id of the tasks have to be specified.
    depends !deliveries.start
  }

  task software "Software Development" {

    # The software is the most critical task of the project. So we set
    # the priority of this task (and all its subtasks) to 1000, the top
    # priority. The higher the priority, the more likely the task will
    # get the requested resources.
    priority 1000

    # All subtasks depend on the specification task.
    depends !spec

    responsible dev1
    task database "Database coupling" {
      effort 20d
      allocate dev1, dev2
      journalentry 2002-02-03 "Problems with the SQL Libary" {
        author dev1
        alert yellow
        summary -8<-
          We ran into some compatibility problems with the SQL
          Library.
        ->8-
        details -8<-
          We have already contacted the vendor and are now waiting for
          their advise.
        ->8-
      }
    }

    task gui "Graphical User Interface" {
      effort 35d
      # This task has taken 5 man-days more than originally planned.
      # We record this as well, so that we can generate reports that
      # compare the delayed schedule of the project to the original plan.
      delayed:effort 40d
      depends !database, !backend
      allocate dev2, dev3
      # Resource dev2 should only work 6 hours per day on this task.
      limits {
        dailymax 6h {
          resources dev2
        }
      }
    }

    task backend "Back-End Functions" {
      effort 30d
      # This task is behind schedule, because it should have been
      # finished already. To document this, we specify that the task
      # is 95% completed. If nothing is specified, TaskJuggler assumes
      # that the task is on schedule and computes the completion rate
      # according to the current day and the plan data.
      complete 95
      depends !database
      allocate dev1, dev2
    }
  }

  task test "Software testing" {

    task alpha "Alpha Test" {
      # Efforts can not only be specified as man-days, but also as
      # man-weeks, man-hours, etc. By default, TaskJuggler assumes
      # that a man-week is 5 man-days or 40 man-hours. These values
      # can be changed, of course.
      effort 1w
      # This task depends on a task in the scope of the enclosing
      # task's enclosing task. So we need two exclamation marks (!!)
      # to get there.
      depends !!software
      allocate test, dev2
      note "Hopefully most bugs will be found and fixed here."
      journalentry 2002-03-01 "Contract with Peter not yet signed" {
        author boss
        alert red
        summary -8<-
          The paperwork is stuck with HR and I can't hunt it down.
        ->8-
        details -8<-
          If we don't get the contract closed within the next week,
          the start of the testing is at risk.
        ->8-
      }
    }

    task beta "Beta Test" {
      effort 4w
      depends !alpha
      allocate test, dev1
    }
  }

  task manual "Manual" {
    effort 10w
    depends !deliveries.start
    allocate doc, dev3
    purge chargeset
    chargeset doc
    journalentry 2002-02-28 "User manual completed" {
      author boss
      summary "The doc writers did a really great job to finish on time."
    }
  }

  task deliveries "Milestones" {

    # Some milestones have customer payments associated with them. We
    # credit these payments to the 'rev' account.
    purge chargeset
    chargeset rev

    task start "Project start" {
      # A task that has no duration is a milestone. It only needs a
      # start or end criterion. All other tasks depend on this task.
      # Here we use the built-in macro ${projectstart} to align the
      # start of the task with the above specified project time frame.
      start ${projectstart}
      # For some reason the actual start of the project got delayed.
      # We record this, so that we can compare the planned run to the
      # delayed run of the project.
      delayed:start 2002-01-20
      # At the beginning of this task we receive a payment from the
      # customer. This is credited to the account associated with this
      # task when the task starts.
      charge 21000.0 onstart
    }

    task prev "Technology Preview" {
      depends !!software.backend
      charge 31000.0 onstart
      note "All '''major''' features should be usable."
    }

    task beta "Beta version" {
      depends !!test.alpha
      charge 13000.0 onstart
      note "Fully functional, may contain bugs."
    }

    task done "Ship Product to Customer" {
      # The next line can be uncommented to trigger a warning about
      # the project being late. For all tasks, limits for the start and
      # end values can be specified. Those limits are checked after the
      # project has been scheduled. For all violated limits a warning
      # is issued.
      # maxend 2002-04-17
      depends !!test.beta, !!manual
      charge 33000.0 onstart
      note "All priority 1 and 2 bugs must be fixed."
    }
  }
}

# Now the project has been specified completely. Stopping here would
# result in a valid TaskJuggler file that could be processed and
# scheduled. But no reports would be generated to visualize the
# results.

navigator navbar {
  hidereport @none
}

macro TaskTip [
  tooltip istask() -8<-
    '''Start: ''' <-query attribute='start'->
    '''End: ''' <-query attribute='end'->
    ----
    '''Resources:'''

    <-query attribute='resources'->
    ----
    '''Precursors: '''

    <-query attribute='precursors'->
    ----
    '''Followers: '''

    <-query attribute='followers'->
    ->8-
]

textreport frame "" {
  header -8<-
    == Accounting Software Project ==
    <[navigator id="navbar"]>
  ->8-
  footer "----"
  textreport index "Overview" {
    formats html
    center '<[report id="overview"]>'
  }

  textreport "Status" {
    formats html
    center -8<-
      <[report id="status.dashboard"]>
      ----
      <[report id="status.completed"]>
      ----
      <[report id="status.ongoing"]>
      ----
      <[report id="status.future"]>
    ->8-
  }

  textreport development "Development" {
    formats html
    center '<[report id="development"]>'
  }

  textreport "Deliveries" {
    formats html
    center '<[report id="deliveries"]>'
  }

  textreport "ContactList" {
    formats html
    title "Contact List"
    center '<[report id="contactList"]>'
  }
  textreport "ResourceGraph" {
    formats html
    title "Resource Graph"
    center '<[report id="resourceGraph"]>'
  }
}

# A traditional Gantt chart with a project overview.
taskreport overview "" {
  header -8<-
    === Project Overview ===

    The project is structured into 3 phases.

    # Specification
    # <-reportlink id='frame.development'->
    # Testing

    === Original Project Plan ===
  ->8-
  columns bsi { title 'WBS' },
          name, start, end, effort, cost,
          revenue, chart { ${TaskTip} }
  # For this report we like to have the abbreviated weekday in front
  # of the date. %a is the tag for this.
  timeformat "%a %Y-%m-%d"
  loadunit days
  hideresource @all
  balance cost rev
  caption 'All effort values are in man days.'

  footer -8<-
    === Staffing ===

    All project phases are properly staffed. See [[ResourceGraph]] for
    detailed resource allocations.

    === Current Status ===

    The project started off with a delay of 4 days. This slightly affected
    the original schedule. See [[Deliveries]] for the impact on the
    delivery dates.
  ->8-
}

# Macro to set the background color of a cell according to the alert
# level of the task.
macro AlertColor [
  cellcolor plan.alert = 0 "#00D000" # green
  cellcolor plan.alert = 1 "#D0D000" # yellow
  cellcolor plan.alert = 2 "#D00000" # red
]

taskreport status "" {
  columns bsi { width 50 title 'WBS' }, name { width 150 },
          start { width 100 }, end { width 100 },
          effort { width 100 },
          alert { tooltip plan.journal
                          != '' "<-query attribute='journal'->" width 150 },
          status { width 150 }
  scenarios delayed

  taskreport dashboard "" {
    headline "Project Dashboard (<-query attribute='now'->)"
    columns name { title "Task" ${AlertColor} width 200},
            resources { width 200 ${AlertColor}
                        listtype bullets
                        listitem "<-query attribute='name'->"
                        start ${projectstart} end ${projectend} },
            alerttrend { title "Trend" ${AlertColor} width 50 },
            journal { width 350 ${AlertColor} }
    journalmode status_up
    journalattributes headline, author, date, summary, details
    hidetask ~hasalert(0)
    sorttasks alert.down, delayed.end.up
    period %{${now} - 1w} +1w
  }
  taskreport completed "" {
    headline "Already completed tasks"
    hidetask ~(delayed.end <= ${now})
  }
  taskreport ongoing "" {
    headline "Ongoing tasks"
    hidetask ~((delayed.start <= ${now}) & (delayed.end > ${now}))
  }
  taskreport future "" {
    headline "Future tasks"
    hidetask ~(delayed.start > ${now})
  }
}

# A list of tasks showing the resources assigned to each task.
taskreport development "" {
  scenarios delayed
  headline "Development - Resource Allocation Report"
  columns bsi { title 'WBS' }, name, start, end, effort { title "Work" },
          duration, chart { ${TaskTip} scale day width 500 }
  timeformat "%Y-%m-%d"
  hideresource ~(isleaf() & isleaf_())
  sortresources name.up
}

# A list of all tasks with the percentage completed for each task
taskreport deliveries "" {
  headline "Project Deliverables"
  columns bsi { title 'WBS' }, name, start, end, note { width 150 }, complete,
          chart { ${TaskTip} }
  taskroot AcSo.deliveries
  hideresource @all
  scenarios plan, delayed
}
# A list of all employees with their contact details.
resourcereport contactList "" {
  scenarios delayed
  headline "Contact list and duty plan"
  columns name,
          email { celltext 1 "[mailto:<-email-> <-email->]" },
          Phone,
          managers { title "Manager" },
          chart { scale day }
  hideresource ~isleaf()
  sortresources name.up
  hidetask @all
}

# A graph showing resource allocation. It identifies whether each
# resource is under- or over-allocated for.
resourcereport resourceGraph "" {
  scenarios delayed
  headline "Resource Allocation Graph"
  columns no, name, effort, rate, weekly { ${TaskTip} }
  loadunit shortauto
  # We only like to show leaf tasks for leaf resources.
  hidetask ~(isleaf() & isleaf_())
  sorttasks plan.start.up
}


Blank
---------
::
/*
 * This file contains a project skeleton. It is part of the
 * TaskJuggler project management tool. You can use this as a basis to
 * start your own project file.
 */
project envc "智能环控器产品开发"  2022-09-01 +12m {
  # Set the default time zone for the project. If not specified, UTC
  # is used.
  timezone "Asia/Shanghai"
  # Hide the clock time. Only show the date.
  timeformat "%Y-%m-%d"
  # Use US format for numbers
  numberformat "-" "" "," "." 1
  # Use US financial format for currency values. Don't show cents.
  currencyformat "(" ")" "," "." 0
  # Pick a day during the project that will be reported as 'today' in
  # the project reports. If not specified, the current day will be
  # used, but this will likely be outside of the project range, so it
  # can't be seen in the reports.
  # now 2011-12-24
  # The currency for all money values is the Euro.
  currency "CNY"

  # You can define multiple scenarios here if you need them.
  #scenario plan "Plan" {
  #  scenario actual "Actual"
  #}

  # You can define your own attributes for tasks and resources. This
  # is handy to capture additional information about the project that
  # is not directly impacting the project schedule, but which you like to
  # keep in one place.
  #extend task {
  #  reference spec "Link to Wiki page"
  #}
  #extend resource {
  #  text Phone "Phone"
  #}
}

copyright "SGI, ltd."

# If you have any text block that you need multiple times to describe
# your project, you should define a macro for it. Macros can even have
# variable segments that you can set upon calling the macro.
#
# macro Task [
#   task "A ${1} task" {
#   }
# ]
#
# Can be called as
# ${Task "big"}
# to generate
# task "A big task" {
# }

# You can attach flags to accounts, resources and tasks. These can be
# used to filter out subsets of them during reporting.
flags important, hidden

# If you want to do budget planning for your project, you need to
# define some accounts.
# account cost "Project Cost" {
#   account dev "Development"
#   account doc "Documentation"
# }
# account rev "Customer Payments"

# The Profit & Loss analysis should be rev - cost accounts.
# balance cost rev

# Define your public holidays here.
vacation "New Year's Day" 2012-01-02
vacation "Birthday of Martin Luther King, Jr." 2012-01-16
vacation "Washington's Birthday" 2012-02-20
vacation "Memorial Day" 2012-05-28
vacation "Independence Day" 2012-07-04
vacation "Labor Day" 2012-09-03
vacation "Columbus Day" 2012-10-08
vacation "Veterans Day" 2012-11-12
vacation "Thanksgiving Day" 2012-11-22
vacation "Christmas Day" 2012-12-25

# The daily default rate of all resources. This can be overridden for each
# resource. We specify this so we can do a good calculation of
# the costs of the project.
# rate 400.0

# This is a set of example resources.
# resource r1 "Resource 1"
# resource t1 "Team 1" {
#   managers r1
#   resource r2 "Resource 2"
#   resource r3 "Resource 3"
# }
# 
# # This is a resource that does not do any work.
# resource s1 "System 1" {
#   efficiency 0.0
#   rate 600.0
# }

task project "智能环控器产品开发" {
  task wp1 "SGI9100" {
    task t1 "开发"
    task t2 "测试"
  }
  task wp2 "SGI9200" {
    depends !wp1
    task t1 "开发"
    task t2 "测试"
    task t3 "试点验证"
  }
  task wp3 "SGI9300" {
    depends !wp1
    task t1 "开发"
    task t2 "测试"
    task t3 "试点验证"
  }  
  task deliveries "Deliveries" {
    task "SGI9200泰安交付" {
      depends !!wp1
    }
    task "SGI9300试点交付" {
      depends !!wp2
    }
  }
}

# Now the project has been specified completely. Stopping here would
# result in a valid TaskJuggler file that could be processed and
# scheduled. Here reports will be generated to visualize the
# results.

navigator navbar {
  hidereport 0
}

macro TaskTip [
  tooltip istask() -8<-
    '''Start: ''' <-query attribute='start'->
    '''End: ''' <-query attribute='end'->
    ----
    '''Resources:'''

    <-query attribute='resources'->
    ----
    '''Precursors: '''

    <-query attribute='precursors'->
    ----
    '''Followers: '''

    <-query attribute='followers'->
    ->8-
]

textreport frame "" {
  header -8<-
    == TaskJuggler Project Template ==
    <[navigator id="navbar"]>
  ->8-
  footer "----"
  textreport index "Overview" {
    formats html
    center '<[report id="overview"]>'
  }

  textreport "Status" {
    formats html
    center -8<-
      <[report id="status.dashboard"]>
      ----
      <[report id="status.completed"]>
      ----
      <[report id="status.ongoing"]>
      ----
      <[report id="status.future"]>
    ->8-
  }

  textreport wps "Work packages" {
    textreport wp1 "Work package 1" {
      formats html
      center '<[report id="wp1"]>'
    }

    textreport wp2 "Work package 2" {
      formats html
      center '<[report id="wp2"]>'
    }
  }

  textreport "Deliveries" {
    formats html
    center '<[report id="deliveries"]>'
  }

  textreport "ContactList" {
    formats html
    title "Contact List"
    center '<[report id="contactList"]>'
  }
  textreport "ResourceGraph" {
    formats html
    title "Resource Graph"
    center '<[report id="resourceGraph"]>'
  }
}

# A traditional Gantt chart with a project overview.
taskreport overview "" {
  header -8<-
    === Project Overview ===

    The project is structured into 2 work packages.

    # Specification
    # <-reportlink id='frame.wps.wp1'->
    # <-reportlink id='frame.wps.wp2'->
    # Testing

    === Original Project Plan ===
  ->8-
  columns bsi { title 'WBS' },
          name, start, end, effort, cost,
          revenue, chart { ${TaskTip} }
  # For this report we like to have the abbreviated weekday in front
  # of the date. %a is the tag for this.
  timeformat "%a %Y-%m-%d"
  loadunit days
  hideresource 1
  balance cost rev
  caption 'All effort values are in man days.'

  footer -8<-
    === Staffing ===

    All project phases are properly staffed. See [[ResourceGraph]] for
    detailed resource allocations.

    === Current Status ===

    Some blurb about the current situation.
  ->8-
}

# Macro to set the background color of a cell according to the alert
# level of the task.
macro AlertColor [
  cellcolor plan.alert = 0 "#00D000" # green
  cellcolor plan.alert = 1 "#D0D000" # yellow
  cellcolor plan.alert = 2 "#D00000" # red
]

taskreport status "" {
  columns bsi { width 50 title 'WBS' }, name { width 150 },
          start { width 100 }, end { width 100 },
          effort { width 100 },
          alert { tooltip plan.journal
                          != '' "<-query attribute='journal'->" width 150 },
          status { width 150 }

  taskreport dashboard "" {
    headline "Project Dashboard (<-query attribute='now'->)"
    columns name { title "Task" ${AlertColor} width 200},
            resources { width 200 ${AlertColor}
                        listtype bullets
                        listitem "<-query attribute='name'->"
                        start ${projectstart} end ${projectend} },
            alerttrend { title "Trend" ${AlertColor} width 50 },
            journal { width 350 ${AlertColor} }
    journalmode status_up
    journalattributes headline, author, date, summary, details
    hidetask ~hasalert(0)
    sorttasks alert.down, plan.end.up
    period %{${now} - 1w} +1w
  }
  taskreport completed "" {
    headline "Already completed tasks"
    hidetask ~(plan.end <= ${now})
  }
  taskreport ongoing "" {
    headline "Ongoing tasks"
    hidetask ~((plan.start <= ${now}) & (plan.end > ${now}))
  }
  taskreport future "" {
    headline "Future tasks"
    hidetask ~(plan.start > ${now})
  }
}

# A list of tasks showing the resources assigned to each task.
taskreport wp1 "" {
  headline "Work package 1 - Resource Allocation Report"
  columns bsi { title 'WBS' }, name, start, end, effort { title "Work" },
          duration, chart { ${TaskTip} scale day width 500 }
  timeformat "%Y-%m-%d"
  hideresource ~(isleaf() & isleaf_())
  sortresources name.up
  taskroot project.wp1
}
# A list of tasks showing the resources assigned to each task.
taskreport wp2 "" {
  headline "Work package 2 - Resource Allocation Report"
  columns bsi { title 'WBS' }, name, start, end, effort { title "Work" },
          duration, chart { ${TaskTip} scale day width 500 }
  timeformat "%Y-%m-%d"
  hideresource ~(isleaf() & isleaf_())
  sortresources name.up
  taskroot project.wp2
}

# A list of all tasks with the percentage completed for each task
taskreport deliveries "" {
  headline "Project Deliverables"
  columns bsi { title 'WBS' }, name, start, end, note { width 150 }, complete,
          chart { ${TaskTip} }
  taskroot project.deliveries
  hideresource 1
}
# A list of all employees with their contact details.
resourcereport contactList "" {
  headline "Contact list and duty plan"
  columns name,
          email { celltext 1 "[mailto:<-email-> <-email->]" },
          managers { title "Manager" },
          chart { scale day }
  hideresource ~isleaf()
  sortresources name.up
  hidetask 1
}

# A graph showing resource allocation. It identifies whether each
# resource is under- or over-allocated for.
resourcereport resourceGraph "" {
  headline "Resource Allocation Graph"
  columns no, name, effort, rate, weekly { ${TaskTip} }
  loadunit shortauto
  # We only like to show leaf tasks for leaf resources.
  hidetask ~(isleaf() & isleaf_())
  sorttasks plan.start.up
}
