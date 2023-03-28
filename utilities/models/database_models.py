from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, UniqueConstraint, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Members(Base):
    __tablename__ = "members"

    member_id = Column(Integer, primary_key=True)
    user_id = Column(String(100), nullable=False)
    username = Column(String(100), nullable=False)
    date_joined = Column(String(100), nullable=False)

    def get_id(self):
        return self.member_id


class Suggestions(Base):
    __tablename__ = "suggestions"

    suggestion_id = Column(Integer, primary_key=True)
    message_id = Column(String(100), nullable=False)
    author_id = Column(String(100), nullable=False)
    content = Column(String(1000), nullable=False)
    up_votes = Column(Integer, nullable=False)
    down_votes = Column(Integer, nullable=False)
    status = Column(String(25), nullable=False)

    unique_votes = relationship("SuggestionVotes", backref="unique_votes", cascade="all, delete")

    def get_id(self):
        return self.suggestion_id


class SuggestionVotes(Base):
    __tablename__ = "suggestion_votes"
    __table_args__ = (UniqueConstraint('suggestion_id', 'voter_id', name='one_vote_per_voter'),)

    suggestion_vote_id = Column(Integer, primary_key=True)
    suggestion_id = Column(Integer, ForeignKey('suggestions.suggestion_id'), nullable=False)
    voter_id = Column(String(100), nullable=False)
    up_vote = Column(Boolean, nullable=False)
    down_vote = Column(Boolean, nullable=False)

    def get_id(self):
        return self.suggestion_vote_id
