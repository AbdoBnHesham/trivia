import React, {Component} from 'react';

import '../stylesheets/App.css';
import Question from './Question';
import Search from './Search';
import $ from 'jquery';

class QuestionView extends Component {
    constructor() {
        super();
        this.state = {
            questions: [],
            page: 1,
            totalQuestions: 0,
            categories: {},
            currentCategory: null,

            handledBy: null,
            selectedCategoryId: null,
            searchTerm: null,
        }
    }

    componentDidMount() {
        this.getQuestions();
    }

    getQuestions = () => {
        $.ajax({
            url: `/api/questions?page=${this.state.page}`,
            type: "GET",
            success: (result) => {
                this.setState({
                    questions: result.questions,
                    totalQuestions: result.total_questions,
                    categories: result.categories,
                    currentCategory: result.current_category,

                    handledBy: null,
                    selectedCategoryId: null,
                    searchTerm: null
                })
                return;
            },
            error: (error) => {
                alert('Unable to load questions. Please try your request again')
                return;
            }
        })
    }

    selectPage(num) {
        this.setState({page: num}, () => {
            //To make sure it paginate with the right endpoint
            if (this.state.handledBy === 'category' && this.state.selectedCategoryId)
                return this.getByCategory(this.state.selectedCategoryId)
            else if (this.state.handledBy === 'search' && this.state.searchTerm)
                return this.submitSearch(this.state.searchTerm)
            this.getQuestions()
        });
    }

    createPagination() {
        let pageNumbers = [];
        let maxPage = Math.ceil(this.state.totalQuestions / 10)
        for (let i = 1; i <= maxPage; i++) {
            pageNumbers.push(
                <span
                    key={i}
                    className={`page-num ${i === this.state.page ? 'active' : ''}`}
                    onClick={() => {
                        this.selectPage(i)
                    }}>{i}
        </span>)
        }
        return pageNumbers;
    }

    getByCategory = (id) => {
        let paginate = this.state.page ? `?page=${this.state.page}` : ''

        $.ajax({
            url: `/api/categories/${id}/questions${paginate}`,
            type: "GET",
            success: (result) => {
                this.setState({
                    questions: result.questions,
                    totalQuestions: result.total_questions,
                    currentCategory: result.current_category,

                    handledBy: 'category',
                    selectedCategoryId: id || null
                })
                return;
            },
            error: (error) => {
                alert('Unable to load questions. Please try your request again')
                return;
            }
        })
    }

    submitSearch = (searchTerm) => {
        $.ajax({
            url: `/api/questions/search`,
            type: "POST",
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                q: searchTerm,
                page: this.state.page || 1
            }),
            xhrFields: {
                withCredentials: true
            },
            crossDomain: true,
            success: (result) => {
                this.setState({
                    questions: result.questions,
                    totalQuestions: result.total_questions,
                    currentCategory: result.current_category,

                    handledBy: 'search',
                    searchTerm
                })
                return;
            },
            error: (error) => {
                alert('Unable to load questions. Please try your request again')
                return;
            }
        })
    }

    questionAction = (id) => (action) => {
        if (action === 'DELETE') {
            if (window.confirm('are you sure you want to delete the question?')) {
                $.ajax({
                    url: `/api/questions/${id}`,
                    type: "DELETE",
                    success: (result) => {
                        this.getQuestions();
                    },
                    error: (error) => {
                        alert('Unable to load questions. Please try your request again')
                        return;
                    }
                })
            }
        }
    }

    render() {
        return (
            <div className="question-view">
                <div className="categories-list">
                    <h2 onClick={() => {
                        this.getQuestions()
                    }}>Categories</h2>
                    <ul>
                        <li onClick={() => this.getQuestions()}>
                            All
                        </li>
                        {Object.keys(this.state.categories).map((id,) => (
                            <li key={id} onClick={() => {
                                this.getByCategory(id)
                            }}>
                                {this.state.categories[id]}
                                <img className="category" src={`${this.state.categories[id]}.svg`}/>
                            </li>
                        ))}
                    </ul>
                    <Search submitSearch={this.submitSearch}/>
                </div>
                <div className="questions-list">
                    <h2>Questions</h2>
                    {this.state.questions.map((q, ind) => (
                        <Question
                            key={q.id}
                            question={q.question}
                            answer={q.answer}
                            category={this.state.categories[q.category]}
                            difficulty={q.difficulty}
                            questionAction={this.questionAction(q.id)}
                        />
                    ))}
                    <div className="pagination-menu">
                        {this.createPagination()}
                    </div>
                </div>

            </div>
        );
    }
}

export default QuestionView;
