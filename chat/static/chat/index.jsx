class App extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            date: new Date()
        };
    }

    componentDidMount() {
        this.timerID = setInterval(() => this.tick(), 1000);
    }

    componentWillUnmount() {
        console.log();
        clearInterval(this.timeID);
    }

    tick() {
        this.setState({
            date: new Date()
        });
    }

    render() {
        return (
            <div>
                <h1>Time: {this.state.date.toLocaleTimeString()}</h1>
            </div>
        );
    }
};


ReactDOM.render(<App />, document.getElementById("app"));


/*
document.addEventListener("DOMContentLoaded", () => {
    const page = window.location.pathname;
    if (page === "/") {
        document.querySelector("#home-link").className = document.querySelector("#home-link").className - "active";
    }
});
*/