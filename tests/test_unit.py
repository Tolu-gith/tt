"""
 TT test
"""
from unittest.mock import AsyncMock, MagicMock, patch, call
import pytest
import ccxt
import iamlistening
from iamlistening import Listener
from fastapi.testclient import TestClient
from tt.bot import app
from tt.utils import (
    listener, parse_message, send_notification,
    load_exchange, execute_order,
    init_message, post_init,
    MessageProcessor, start_plugins,
    trading_switch_command, get_name, get_quote, get_trading_asset_balance,
    get_account, get_account_balance,
    get_account_position,
    get_account_margin,
    get_host_ip, get_ping,)
from tt.config import settings, logger
from tt.plugins.example_plugin import ExamplePlugin



@pytest.fixture(scope="session", autouse=True)
def set_test_settings():
    settings.configure(FORCE_ENV_FOR_DYNACONF="testing")

@pytest.fixture(name="settings_cex")
def set_test_settings_CEX():
    settings.configure(FORCE_ENV_FOR_DYNACONF="testing_cex")

@pytest.fixture(name="settings_dex_56")
def set_test_settings_DEX56():
    settings.configure(FORCE_ENV_FOR_DYNACONF="testing_dex_56")

@pytest.fixture(name="settings_dex_10")
def set_test_settings_DEX10():
    settings.configure(FORCE_ENV_FOR_DYNACONF="testing_dex_10")

def test_dynaconf_is_in_testing_env_CEX(settings_cex):
    print(settings.VALUE)
    assert settings.VALUE == "On Testing CEX_binance"
    assert settings.cex_name == "binance"
    assert settings.cex_api == 'api_key'

def test_dynaconf_is_in_testing_env_DEX56(settings_dex_56):
    print(settings.VALUE)
    assert settings.VALUE == "On Testing DEX_56"
    assert settings.cex_name == ""
    assert settings.dex_wallet_address == "0x1234567890123456789012345678901234567899"

def test_dynaconf_is_in_testing_env_DEX10(settings_dex_10):
    print(settings.VALUE)
    assert settings.VALUE == "On Testing DEX_10"
    assert settings.cex_name == ""
    assert settings.dex_wallet_address == "0x1234567890123456789012345678901234567899"

@pytest.fixture(name="message")
def message_fixture():
    return "hello"

@pytest.fixture(name="command")
def command_message():
    return "/help"

@pytest.fixture(name="order")
def order_params():
    """Return order parameters."""
    return {
        'action': 'BUY',
        'instrument': 'EURUSD',
        'quantity': 1,
        # other order parameters
    }


@pytest.mark.asyncio
async def test_listener_discord(settings_dex_56):
    print(settings.VALUE)
    listener = Listener()
    print(listener)
    assert listener is not None
    assert isinstance(listener, iamlistening.main.Listener)

@pytest.mark.asyncio
async def test_listener_telegram(message):
    listener = Listener()
    print(listener)
    assert listener is not None
    assert isinstance(listener, iamlistening.main.Listener)
    await listener.handle_message(message)
    msg = await listener.get_latest_message()
    print(msg)
    assert msg == "hello"

@pytest.mark.asyncio
async def test_listener_matrix(settings_dex_10):
    listener = Listener()
    print(listener)
    assert listener is not None
    assert isinstance(listener, iamlistening.main.Listener)

@pytest.mark.asyncio
async def test_parse_help():
    """Test parse_message balance """
    send_notification_mock = AsyncMock()
    with patch('tt.utils.send_notification',send_notification_mock):
        await load_exchange()
        await parse_message('/help')
        assert '🏦' in send_notification_mock.call_args[0][0]


# @pytest.mark.asyncio
# async def test_parse_bal():
#     """Test parse_message balance """
#     send_notification_mock = AsyncMock()
#     with patch('tt.utils.send_notification',send_notification_mock):
#         await load_exchange()
#         await parse_message('/bal')
#         assert '🏦' in send_notification_mock.call_args[0][0]


# @pytest.mark.asyncio
# async def test_parse_quote(mock_dex):
#     """Test parse_message balance """
#     send_notification_mock = AsyncMock()
#     get_quote_mock = AsyncMock(return_value={'symbol': 'WBTC'})
#     with patch('tt.utils.send_notification',send_notification_mock):
#         with patch('tt.utils.get_quote',get_quote_mock):
#             await load_exchange()
#             result = await parse_message('/quote WBTC')
#             get_quote_mock.assert_called_once_with('WBTC')


@pytest.mark.asyncio
async def test_parse_trading():
    """Test parse_message balance """
    send_notification_mock = AsyncMock()
    with patch('tt.utils.send_notification',send_notification_mock):
        await load_exchange()
        await parse_message('/trading')
        assert 'Trading is' in send_notification_mock.call_args[0][0]


@pytest.mark.asyncio
async def test_send_notification(caplog, settings_dex_56):
    """Test send_notification function"""
    send_notification_mock = AsyncMock()
    with patch('tt.utils.send_notification',send_notification_mock):

        message = '<code>test message</code>'

        output = await send_notification(message)
        print(output)
        assert 'https://discord.com/api/webhooks/12345678901/1234567890' in caplog.text


@pytest.mark.asyncio
async def test_get_host_ip():
    """Test get_host_ip """
    output = get_host_ip()
    assert output is not None


@pytest.mark.asyncio
async def test_dex_load_exchange():
    """test exchange dex"""
    exchange = await load_exchange()
    print(exchange)
    assert exchange is not None


@pytest.mark.asyncio
async def test_cex_load_exchange(settings_cex):
    """test exchange cex"""
    mock_ccxt = MagicMock()
    mock_ccxt.cex_client = MagicMock()
    mock_exchange = MagicMock()
    with patch.dict("sys.modules", ccxt=mock_ccxt):
        mock_ccxt.cex_client.return_value = mock_exchange
        result = await load_exchange()
        name = await get_name()
        assert result is not None
        assert name == 'binance'
        assert isinstance(result, ccxt.binance)


# @pytest.mark.asyncio
# async def test_successful_execute_order(caplog, order_params, mock_dex):
#     await load_exchange()
#     dex_execute_mock = AsyncMock()
#     with patch('dxsp.execute_order',dex_execute_mock):
#         trade_confirmation = await execute_order(order_params)

#         # Assert that no warning is logged
#         assert "execute_order:" not in caplog.text
#         # Assert that no notification is sent
#         assert "⚠️ order execution:" not in caplog.text
#         # Assert that the trade confirmation is returned
#         assert isinstance(trade_confirmation, str)
#         # Add more specific assertions for the trade confirmation if needed
#         assert "⬇️" in trade_confirmation or "⬆️" in trade_confirmation
#         assert "Size:" in trade_confirmation
#         assert "Entry:" in trade_confirmation
#         assert "ℹ️" in trade_confirmation
#         assert "🗓️" in trade_confirmation



@pytest.mark.asyncio
async def test_failed_execute_order(caplog, order):
    await load_exchange()
    trade_confirmation = await execute_order(order)
    assert 'Order execution failed' in caplog.text


@pytest.mark.asyncio
async def test_get_quote():
    """Test get_quote """
    await load_exchange()
    output = await get_quote("WBTC")
    print(output)
    assert output is not None


@pytest.mark.asyncio
async def test_get_name(settings_cex):
    """Test get_name function."""
    await load_exchange()
    output = await get_name()
    print(output)
    assert output is not None

@pytest.mark.asyncio
async def test_get_account_balance():
    """Test get_account_balance."""
    await load_exchange()
    output = await get_account_balance()
    print(output)
    assert output is not None


@pytest.mark.asyncio
async def test_get_trading_asset_balance():
    """Test get_asset_trading_balance."""
    await load_exchange()
    output = await get_trading_asset_balance()
    print(output)
    assert output is not None

    
@pytest.mark.asyncio
async def test_get_account_position():
    """Test get_account_positions."""
    await load_exchange() 
    output = await get_account_position()
    print(output)
    assert output is not None


@pytest.mark.asyncio
async def test_get_account_margin():
    """Test get_account_margin """
    await load_exchange() 
    output = await get_account_margin()
    print(output)
    assert output is not None


@pytest.mark.asyncio
async def test_init_message():
    """Test test_init_message."""
    await load_exchange()
    output = await init_message()
    print(output)
    assert output is not None


@pytest.mark.asyncio
async def test_toggle_trading_active():
    print(settings.trading_enabled)
    await trading_switch_command()
    print(settings.trading_enabled)
    assert settings.trading_enabled is False

def test_read_main():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200

def test_read_health():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200

def test_webhook_with_valid_payload():
    client = TestClient(app)
    payload = {"key": "my_secret_key", "data": "my_data"}
    response = client.post("/webhook", json=payload)
    assert response is not None
