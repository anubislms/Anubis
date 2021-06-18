import React from 'react';
import Typography from '@material-ui/core/Typography';
import Link from '@material-ui/core/Link';
import CardMedia from '@material-ui/core/CardMedia';

import BlogPost from './BlogPost';
import BlogImg from './BlogImg';

function Preview({classes}) {
  return (
    <>
      <div style={{display: 'flex', justifyContent: 'center', marginBottom: 20, height: 350}}>
        <img src={'/logo512.png'} alt={'logo'}/>
      </div>

      <Typography gutterBottom className={classes.subtitle} style={{marginTop: 0}}>
        What you gain by using Anubis
      </Typography>
      <Typography gutterBottom className={classes.typography}>
        There are 4 main benefits to using Anubis.
        <ul>
          <li>
            Students can edit and run their code right in their browser. No class VMs, nothing to install.
          </li>
          <li>Students get live feedback on their answers <i>before</i> the deadline</li>
          <li>The feedback given to students is then used to help speed up TAs grading</li>
          <li>
            The data generated by the platform can be used to get
            insight into everything from which things the class is struggling with
            to when students actually start and how long they spend on an assignment
          </li>
        </ul>
      </Typography>
      <Typography gutterBottom className={classes.typography}>
        For the Introduction to Operating Systems course, the combination of these
        benefits both from the perspective of the student and TA has resulted in
        an overall increase in the average grade of the class. The feedback the
        students get help them to see where their errors are before they hand in
        their work. Then the usage data generated by the platform helps the TAs and
        professor make decisions about which material students are and are not
        understanding.
      </Typography>
    </>
  );
}

function Post({classes}) {
  return (
    <>
      <Typography className={classes.typography}>
        At its core, Anubis is a tool to give students live feedback from their homework
        assignments
        while they are working on them. Using <Link target={'_blank'} href={'https://classroom.github.com/'}>
        Github Classrooms</Link>,
        each student gets their
        own repo from a template
        for each homework assignment. The way students then submit their work
        is simply by pushing their work to their repo before the deadline. Students can
        then push, and therefore submit as many times as
        they would like before the deadline.
      </Typography>


      <Typography gutterBottom color={'textSecondary'} className={classes.subtitle}>
        Anubis Cloud IDEs
      </Typography>
      <Typography gutterBottom className={classes.typography}>
        New in version v2.2.0, there is now the Anubis Cloud IDE. Using some
        kubernetes magic, we are able to
        host <Link target={'_blank'} href={'https://theia-ide.org/'}>
        Theia</Link> servers for individual students.
        These are essentially VSCode instances
        that students can access in the browser. What makes these so powerful
        is that students can access a terminal
        and type commands right into a bash shell which will be run in the
        remote container. With this setup students
        have access to a fully insulated and prebuilt linux
        environment at a click of a button. These environments are easily customizable
        for the needs of the class or even individual assignments. Because these
        IDE servers are light weight docker containers we can support
        many more students than if we used VMs. There are ~130 students in the Intro
        to OS course in spring of 2021, and we could support all of them
        using IDEs at the same time while still processing all the submissions that
        come through.
      </Typography>
      <Typography gutterBottom className={classes.typography}>
        As we are giving students access to a terminal in the cloud, we must also lock
        down their environment. All student IDEs are limited in the RAM, CPU, storage,
        and networking. From the IDEs, students are only able to connect to Github to
        submit their work.
      </Typography>
      <BlogImg
        alt={'theia-fullscreen.png'}
        src="/api/public/static/c99e89d478b73ad6"
      />

      <Typography gutterBottom color={'textSecondary'} className={classes.subtitle}>
        Assignments on Anubis
      </Typography>
      <Typography gutterBottom className={classes.typography}>
        When a student pushes to their assignment repo, a job is launched on the Anubis
        cluster. That job will build
        their repo, run tests on the results, and store the results in a database.
      </Typography>
      <Typography gutterBottom className={classes.typography}>
        Students can then navigate to the Anubis website, where
        they will sign in through NYU SSO.
        From there,
        they will be able to see all the current and past assignments,
        and all of their submissions. They are able
        to view the results of the build and tests for each submission.
        There they can request a regrade,
        there by launching a new submission pipeline. While the submission
        still being processed, the website will poll
        the backend for updates. In this, the website will be constantly
        updating while the submission is being
        processed, giving a live and interactive feel to the site. Once
        a submission is processed Anubis will show
        the students logs from their tests, and builds along with which
        tests passed and which failed.
      </Typography>
      <BlogImg
        alt={'theia-fullscreen.png'}
        src="/api/public/static/82255026ec8ec6d2"
      />

      <Typography gutterBottom className={classes.subtitle}>
        Usage Data
      </Typography>
      <Typography gutterBottom className={classes.typography}>
        Given the structure of Anubis assignments, coupled with the Anubis Cloud IDEs
        track and measure when students start and finish their assignments, and how long
        it takes them to pass specific tests. In the autograde results panel, a &quot;visual
        history&quot; is generated for each student. It shows when students started their
        assignment, then for each submission if their build passed or failed and how many
        tests passed. If they used the Anubis Cloud IDEs as most students do choose to, then
        the graph generated shows a <i>near minute by minute</i> representation of which challenges
        they faced and how long it took for them to overcome them.
      </Typography>
      <BlogImg
        alt="student assignment visual history"
        src="/api/public/static/000e6a27e2f9a14d"
      />
      <Typography className={classes.sidebar}>
        This example shows the build as the green line, and the assignment tests as the blue line.
        We can see that this student spent a good deal of time on the first day just getting their
        tests to pass, only to revisit their work the next day probably to clean up their submission.
      </Typography>

      <Typography gutterBottom className={classes.typography}>
        Then more generally Anubis can represent how the class as a whole did on
        the assignment. One of the core visuals generated is what we call the
        &quot;summary sundial&quot;. In this sundial, we can
        show a quick view of how well the class did on the assignment.
      </Typography>
      <BlogImg
        alt="sundial1"
        src='/api/public/static/a9e88ca0a6b55d34'
      />
      <Typography gutterBottom className={classes.sidebar}>
        The sundial shows how many students submitted work, and which test had the most cases pass.
        This assignment had 5 autograde tests. The inner purple radial represents all the students that
        submitted work for this assignment. Then each of the outer 5 blue radials represents an assignment
        test. Then the most outside layer shows in green and red how many students passed, and failed
        that test. We can hover over an element to get a more detailed look.
      </Typography>


      <Typography gutterBottom className={classes.subtitle}>Autograding</Typography>
      <Typography gutterBottom className={classes.typography}>
        The generated autograde results are available to TAs and Professors all
        from the Anubis admin panel. Student results are automatically indexed
        searchable. Having these results greatly increase the speed that TAs
        grade.
      </Typography>

      <Typography gutterBottom className={classes.typography}></Typography>

      <Typography gutterBottom className={classes.typography}>
        Does any of this sound appealing to you? Reach out to us to see if Anubis is
        something that can benefit your class!
      </Typography>
    </>
  );
}

export default function ElevatorPitch(props) {
  return (
    <BlogPost
      Preview={Preview}
      Post={Post}
      title={'Anubis LMS'}
      author={'John Cunniff'}
      date={'2021-03-17'}
      {...props}
    />
  );
}
