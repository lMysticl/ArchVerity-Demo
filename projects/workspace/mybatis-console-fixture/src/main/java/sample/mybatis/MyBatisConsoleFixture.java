package sample.mybatis;

public final class MyBatisConsoleFixture {
    private MyBatisConsoleFixture() {
    }

    public static void main(String[] args) {
        System.out.println("Preparing: SELECT * FROM payments WHERE id = ? AND status = ?");
        System.out.println("Parameters: 42(Long), O'Reilly(String)");
    }
}
