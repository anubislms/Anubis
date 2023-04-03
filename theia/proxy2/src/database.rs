use crate::error::DBError;

use sqlx::{
    mysql::{MySql, MySqlPool, MySqlPoolOptions, MySqlConnectOptions},
    pool::PoolConnection,
};
use futures::executor::block_on;


#[derive(Debug)]
#[derive(sqlx::FromRow)]
pub struct User {
    id: String,
    name: String,
}


#[derive(Debug)]
#[derive(sqlx::FromRow)]
pub struct IDESession {
    pub id: String,
    pub active: bool,
    pub cluster_address: String,
}

#[derive(Clone, Debug)]
pub struct AnubisDB {
    pool: MySqlPool
}


impl AnubisDB {
    pub fn new(
        db_user: &str,
        db_password: &str,
        db_host: &str,
        db_database: &str,
        db_port: u16,
        max_connections: u32,
    ) -> AnubisDB {

        tracing::info!("Init Database");
        tracing::info!("db_user         = {:?}", db_user);
        tracing::info!("db_host         = {:?}", db_host);
        tracing::info!("db_database     = {:?}", db_database);
        tracing::info!("db_port         = {:?}", db_port);
        tracing::info!("max_connections = {:?}", max_connections);

        // Create connect options
        let options = MySqlConnectOptions::new()
        .username(db_user)
        .password(db_password)
        .host(db_host)
        .database(db_database)
        .port(db_port);

        // Create pool Result value
        let pool = block_on(MySqlPoolOptions::new()
        .max_connections(max_connections)
        .connect_with(options));

        AnubisDB {
            pool: pool.expect("Unable to connect to db")
        }
    }

    fn get_connection(&self) -> PoolConnection<MySql> {
        let fut = self.pool.acquire();
        block_on(fut).expect("Could not acquire connection")
    }

    pub fn get_session(&self, session_id: &str) -> Result<IDESession, DBError> {
        let mut conn = self.get_connection();
        let stream = sqlx::query_as::<_, IDESession>("SELECT * FROM theia_session WHERE id = ? AND active = ?;")
        .bind(session_id)
        .bind(1)
        .fetch_one(&mut conn);

        match block_on(stream) {
            Err(e) => Err(DBError{message: e.to_string()}),
            Ok(v) => Ok(v),
        }
    }   
}

