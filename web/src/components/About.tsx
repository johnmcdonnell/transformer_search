import React from 'react';

import { Typography, Box, Paper, Container, List, ListItem, Link } from '@mui/material';


class About extends React.Component {
    render() {
      return (
        <Container maxWidth="sm">
            <Paper
                elevation={3}
                sx={{
                    p: 2,
                    m: 2,
                    display: 'flex',
                    flexDirection: 'column',
                    textAlign: 'left',
                }}
            >
                <Typography variant="h3" gutterBottom>
                    About
                </Typography>
                <div style={{position: "relative", paddingBottom: "64.90384615384616%", height: "0"}}>
                    <iframe title='Demo Video' src="https://www.loom.com/embed/e307765429db4fe38efd2fc822bb4529" frameBorder="0"  style={{position: "absolute", "top": 0, left: 0, width: "100%", height: "100%"}}>
                        </iframe>
                    </div>
                <Box sx={{ m: 2 }} />
                <Typography variant="body1" gutterBottom>
                    Vibecheck is an AI native knowledge retrieval tool that organizes the world's personally trusted information.
                    Vibecheck is currently indexing the <Link href="https://marginalrevolution.com/marginalrevolution/">Marginal Revolution blog</Link>, a source the creators deeply trust.
                </Typography>
                <Typography variant="body1" gutterBottom>
                    Vibecheck uses the <Link href="https://www.sbert.net/">Sentence Transformers library</Link> to encode MR posts into vectors, and identifies relevant posts using vector distance to the query.
                    GPT-3 is then used to summarize the information in the posts.
                    This is the start of a general-purpose knowledge retrieval tool.
                </Typography>
                <Typography variant="body1" gutterBottom>
                    The vision is to expand Vibecheck to index a wide variety of sources, and to provide a platform for users to share their own trusted sources.
                </Typography>
                
                <Box sx={{ m: 2 }} />
                <Typography variant="h5" gutterBottom>
                    Contributors
                </Typography>
                <List dense={true} >
                    <ListItem>
                        <Typography variant="body1">
                            Creator: John McDonnell
                            [<Link href="https://twitter.com/johnmcdonnell">Twitter</Link>]
                            [<Link href="https://www.linkedin.com/in/john-mcdonnell-65833233/">LinkedIn</Link>]
                        </Typography>
                    </ListItem>
                    <ListItem>
                        <Typography variant="body1">
                            Chief catalyst: Bryan Davis
                            [<Link href="https://twitter.com/gilbertgravis">Twitter</Link>]
                            [<Link href="https://www.linkedin.com/in/bryangilbertdavis//">LinkedIn</Link>]
                        </Typography>  
                    </ListItem>
                </List>

            </Paper>
        </Container>

        );
    }
  }


export default About;