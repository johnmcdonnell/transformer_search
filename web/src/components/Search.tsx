import React from 'react'
import Moment from 'react-moment';

import Typography from '@mui/material/Typography'
import { Box, Button, Input, Paper, Container, List, ListItem, Link, CircularProgress } from '@mui/material';

const backend_url = 'https://johnmcdonnell-transformer-search-backend-fastapi-app.modal.run'

// const sham_results = {"results":[{"result_number":1,"score":{},"title":"The balance sheet recession and The Great Stagnation",
// "author":"Tyler Cowen","date":"2012-02-25 08:08:56","content":"\nMany people point out that we are in a balance sheet recession.  I agree with this view but wish to push it one step deeper.  The negative wealth and income effects on debtors are positive wealth and income effects for the creditors.  If the creditors were keener to invest that money in useful, productive activities the economy would be much stronger.  Balance sheet recessions are most problematic when the investment channel is for some reason broken or especially weak.\nYou might think “Ah, the weak investment channel is due to weak AD.”  And in part it is.  But, if I may quote the Austrians, production takes time and recoveries do not take forever.  Investors are often keen to invest into the swoosh of a future, not too far away, post-recession boom.  But this desire has been much weaker than in many times past.  A lot of the weakness of AD comes from the investment side, and in fact it predated the recession.\n\n","link":"https://marginalrevolution.com/marginalrevolution/2012/02/the-balance-sheet-recession-and-the-great-stagnation.html"},{"result_number":2,"score":{},"title":"Noah Smith on the Gennaioli and Shleifer theory of the great recession","author":"Tyler Cowen","date":"2018-07-31 02:00:39","content":"\nGennaioli and Shleifer explain these patterns by turning to their own preferred theory of human irrationality — the theory of extrapolative expectations. Basically, this theory holds that when asset prices rise — home values, stocks and so on — without a break, investors start to believe that this trend represents a new normal. They pile into the asset, pumping up the price even more, and seeming to confirm the idea that the trend will never end. But when the extrapolators’ money runs out, reality sets in and a crash ensues. Gennaioli, Shleifer, and their coauthors have been only one of several teams of researchers to investigate this idea and its implications in recent years.\nWhen extrapolative expectations are combined with an inherently fragile financial system, a predictable cycle of booms and busts is the result. At some point during good economic times, irrational exuberance takes hold, pushing stock prices, house values, or both into the stratosphere. When they inevitably come down, banks collapse, taking the rest of the economy with them.\nHere is his full Bloomberg column.  Here slides from the authors.\n","link":"https://marginalrevolution.com/marginalrevolution/2018/07/noah-smith-gennaioli-shleifer-theory-great-recession.html"},{"result_number":3,"score":{},"title":"Did “minority lending” drive the crisis?","author":"Tyler Cowen","date":"2008-09-30 11:25:01","content":"\nThis is one of the queries I receive, in varying forms, every day.  Did policies such as the Community Reinvestment Act significantly worsen the housing bubble and the subsequent collapse?  Basically not, although in my view these were bad policies for other reasons.  They contributed to our current problems by only a small amount and of course these policies have been around for a long time before the housing bubble ever got started.  Here is one back-of-the-envelope debunking of the \"diversity recession\" idea.  Matt Yglesias links to some other debunkings.\nYou can, however, cite the general obsession with extending home ownership as strong evidence that putting Democrats in charge does not suffice to solve our regulatory problems.\nOnly polite comments will be left standing…\n","link":"https://marginalrevolution.com/marginalrevolution/2008/09/did-minority-le.html"},{"result_number":4,"score":{},"title":"Did the debt ceiling dispute hurt the economy?","author":"Tyler Cowen","date":"2012-05-30 02:33:24","content":"\nMatt offers a summary with links:\nI was hoping to do a followup piece on that point, but Betsey Stevenson and Justin Wolfers did a great one for Bloomberg yesterday. The basic point is that we had three of the worst months for job growth of the entire recovery while the debate played out and consumer confidence took a sharp but temporary tumble. This was, in other words, just about the only time from the stress tests until the present when you seemed to see a real sense of panic and uncertainty afflicting the economy. The whole rest of the period has been pretty bad anyway, but the debt ceiling debate really dealt us a blow.\n","link":"https://marginalrevolution.com/marginalrevolution/2012/05/did-the-debt-ceiling-dispute-hurt-the-economy.html"},{"result_number":5,"score":{},"title":"A Great Depression for rich people","author":"Tyler Cowen","date":"2009-02-27 05:55:00","content":"\nWhat does a Great Depression for the relatively wealthy look like?  If you spend lots of your budget on  \"luxuries\" — especially durables — it is easy to postpone their consumption.  This might cause gdp to fall more rapidly than if people were poorer.  If you are spending most of your money to eat and stay alive, and a negative shock comes, you have to work harder to make up the difference.\nIt's so, so easy to put off the purchase of a new car.  And that makes for a steep ride down, most of all for the geographically distant producers of durable goods.  Whether the steep economic plunge is worse in utility terms is debatable but maybe not because wealth buffers are better built up.\nOn the other hand, the presence of so many wonderful free goods allows for easy substitution into activities which do not generate much economic revenue or employment.\nFor these ideas I am indebted to a conversation with Arnold Kling and Seth Ditchik, just before we ate superb barbecue at Oklahoma Joe's, get the ribs and french fries.\n","link":"https://marginalrevolution.com/marginalrevolution/2009/02/a-great-depression-for-rich-people.html"}],
// "summary": "Article 1:\n    \n    The article discusses the views of Nobel Laureate Joseph Brodsky on Ukraine. Brodsky believed that Ukraine was not a separate nation from Russia, and that the independence of Ukraine was a mistake. He also thought that Ukraine should be part of Russia.\n    \nArticle 2:\n    \n    The article discusses how the IR community got Russia/Ukraine so wrong. It argues that the community did not foresee the war in Ukraine because they did not understand the historical continuity and persistence of Russian involvement in Ukraine.\n    \n    Article 3:\n \n    The article discusses how Putin's beliefs about history justify Russian expansionism. It argues that Putin's ideas about history are a continuation of a longstanding tradition in Russian leadership." }

type SearchProps = {
    query: string,
    results: Array<{
        result_number: number,
        title: string,
        author: string,
        date: string,
        content: string,
        link: string,
    }>,
    summary: string,
    loading_hits: boolean,
    loading_summary: boolean,
}



class Results extends React.Component<{results: SearchProps['results']}> {
    render() {
        if (this.props.results.length > 0) {

            return (
                <Container sx={{margin: '2em auto'}}
                >
                    <Typography
                        variant="h3"
                        color='text.secondary'
                    >
                        Hits
                    </Typography>
                    <List sx={{backgroundColor: 'secondary.main', 'borderRadius': '10px'}}>
                        {this.props.results.map((result) => <ListItem key={result.result_number}><SearchResult result={result} /></ListItem>)}
                    </List>
                </Container>
            )
        } else {
            return ('')
        }
    }
}


class Summary extends React.Component<{summary: string, loading: boolean}> {

    render() {
        if (this.props.summary.length > 0 || this.props.loading) {
            return (
                <Container>
                    <Typography
                    variant="h3"
                    color='text.secondary'
                >
                    🤖Summary🤖
                    </Typography>
                    <Paper sx={{backgroundColor: 'secondary.main', 'borderRadius': '10px', m: '0 auto', p: '1em', width: '80%'}}>
                        {this.props.loading && <CircularProgress /> }
                        <Typography variant="body2" sx={{'textAlign': 'justify', 'whiteSpace': 'pre-line'}}>
                            {this.props.summary}
                        </Typography>
                    </Paper>
                </Container>
            )
        } else {
            return ('')
        }
    }
}


function SearchResult(props: {'result': SearchProps['results'][0]}) {
    return (
        <Paper elevation={3} sx={{
            m: '1em',
            p: '1em',
        }}>
            <Link
                href={props.result.link}
                variant="h6" gutterBottom 
            >
                {props.result.title}
            </Link>
            <Typography variant="body2" gutterBottom>
                <strong>Author</strong> {props.result.author}
            </Typography>
            <Typography variant="body2" gutterBottom>
            <Moment date={props.result.date} format="YYYY-MM-DD"></Moment> (<Moment fromNow>{props.result.date}</Moment>)
            </Typography>
            <Typography variant="body2" gutterBottom>
                {props.result.content}
            </Typography>
            <Typography variant="body2" gutterBottom>
            </Typography>
        </Paper>
    )
}

class Search extends React.Component<{}, SearchProps> {
    constructor(props: SearchProps) {
        super(props);
        this.state = {
            query: '',
            results: [],
            summary: '',
            loading_hits: false,
            loading_summary: false,
        }
    }

    fetch_summary = () => {
        this.setState({loading_summary: true})
        fetch(`${backend_url}/summarize_results`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    query: this.state.query,
                    hit_uris: this.state['results'].map((result) => result.link)
                    })
            })
            .then(response => response.json())
            .then(data => this.setState({summary: data['summary'],
                                         loading_summary: false}))
            .catch((error) => {
                console.error('Error fetching summary:', error);
            });
    }


    fetch_hits() {
        this.setState({'loading_hits': true,
                       'loading_summary': true}) 
        fetch(`${backend_url}/search?query_string=${this.state.query}`)
            .then(response => response.json())
            .then(data => this.setState({'results': data.results, 'loading_hits': false}))
            .then(this.fetch_summary)
            .catch((error) => {
                console.error('Error fetching hits:', error);
            });

    }

    setSearch(search: string) {
        this.setState({query: search})
    }

    render () {
        const {results, summary, loading_hits, loading_summary} = this.state;
        return (
            <div>
                <form 
                    onSubmit={(e) => {
                        e.preventDefault();
                        this.fetch_hits()
                    }}
                >
                    <Input
                        placeholder="Search"
                        disableUnderline
                        onChange={(e) => this.setSearch(e.target.value)}
                        autoFocus={true}
                        sx={{backgroundColor: 'secondary.main', m: '1em', p: '.5em', width: '60%', color: 'text.primary', 'borderRadius': '1em'}}
                    />
                    <Button
                        type="submit"
                        variant="contained"
                        disabled={loading_hits}
                    >
                        {loading_hits ? 'Loading…' : 'Semantic Search' }
                    </Button>
                </form>
                <Box sx={{ m: 2 }} />
                <Summary summary={summary} loading={loading_summary} />
                <Results results={results} />
            </div>
        )   
    
    } 
}

export default Search;
