import * as React from "react"
import {Layout} from '../components'
import {Showcase, HotFeatures} from '../components/molecules';
import {PrimaryButton, SecondaryButton} from "../components/atoms";
import {navigate} from 'gatsby';

export const Home = () => {
  return (
    <Layout>
      <link rel="preload" href="/fonts/GoshaSans-Bold.woff" as="font" type="font/woff" crossOrigin />
      <link rel="preload" href="/fonts/GoshaSans-Bold.woff2" as="font" type="font/woff2" crossOrigin />
      <div className= 'flex flex-col max-w-5xl items-center justify-center text-center space-y-32'>
        <div>
          <h1 className= 'text-6xl font-gosha font-bold '>Completely Automate your Course</h1>
          <div className= 'space-x-4 mt-12'>
            <PrimaryButton>Request A Demo</PrimaryButton>
            <SecondaryButton onClick = {() => navigate('/features')}>Learn More</SecondaryButton>
          </div>
        </div>
        <Showcase />
        <HotFeatures />

      </div>
    </Layout>
  )
}

export default Home;
