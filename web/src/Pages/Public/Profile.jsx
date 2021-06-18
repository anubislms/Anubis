import React, {useState} from 'react';

import {Redirect} from 'react-router-dom';

import Grid from '@material-ui/core/Grid';
import CircularProgress from '@material-ui/core/CircularProgress';

import useGet from '../../hooks/useGet';
import ProfileCard from '../../Components/Public/Profile/ProfileCard';
import StandardLayout from '../../Components/Layouts/StandardLayout';


export default function Profile() {
  const [_github_username, set_github_username] = useState(null);
  const [{loading, error, data}] = useGet('/api/public/auth/whoami');

  if (loading) return <CircularProgress/>;
  if (error) return <Redirect to={`/error`}/>;

  const {user} = data;

  const github_username = _github_username || user.github_username;

  return (
    <StandardLayout description={'Profile'}>
      <Grid container spacing={4} justify={'center'}>
        <Grid item xs={12} sm={10} md={8} lg={4}>
          <ProfileCard
            user={user}
            github_username={github_username}
            set_github_username={set_github_username}
          />
        </Grid>
      </Grid>
    </StandardLayout>
  );
}

