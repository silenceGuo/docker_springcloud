/*
 * Generated by the Jasper component of Apache Tomcat
 * Version: Apache Tomcat/8.5.8
 * Generated at: 2018-06-20 06:07:02 UTC
 * Note: The last modified time of this file was set to
 *       the last modified time of the source file after
 *       generation to assist with modification tracking.
 */
package org.apache.jsp.WEB_002dINF.error;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;

public final class _404_jsp extends org.apache.jasper.runtime.HttpJspBase
    implements org.apache.jasper.runtime.JspSourceDependent,
                 org.apache.jasper.runtime.JspSourceImports {

  private static final javax.servlet.jsp.JspFactory _jspxFactory =
          javax.servlet.jsp.JspFactory.getDefaultFactory();

  private static java.util.Map<java.lang.String,java.lang.Long> _jspx_dependants;

  private static final java.util.Set<java.lang.String> _jspx_imports_packages;

  private static final java.util.Set<java.lang.String> _jspx_imports_classes;

  static {
    _jspx_imports_packages = new java.util.HashSet<>();
    _jspx_imports_packages.add("javax.servlet");
    _jspx_imports_packages.add("javax.servlet.http");
    _jspx_imports_packages.add("javax.servlet.jsp");
    _jspx_imports_classes = null;
  }

  private volatile javax.el.ExpressionFactory _el_expressionfactory;
  private volatile org.apache.tomcat.InstanceManager _jsp_instancemanager;

  public java.util.Map<java.lang.String,java.lang.Long> getDependants() {
    return _jspx_dependants;
  }

  public java.util.Set<java.lang.String> getPackageImports() {
    return _jspx_imports_packages;
  }

  public java.util.Set<java.lang.String> getClassImports() {
    return _jspx_imports_classes;
  }

  public javax.el.ExpressionFactory _jsp_getExpressionFactory() {
    if (_el_expressionfactory == null) {
      synchronized (this) {
        if (_el_expressionfactory == null) {
          _el_expressionfactory = _jspxFactory.getJspApplicationContext(getServletConfig().getServletContext()).getExpressionFactory();
        }
      }
    }
    return _el_expressionfactory;
  }

  public org.apache.tomcat.InstanceManager _jsp_getInstanceManager() {
    if (_jsp_instancemanager == null) {
      synchronized (this) {
        if (_jsp_instancemanager == null) {
          _jsp_instancemanager = org.apache.jasper.runtime.InstanceManagerFactory.getInstanceManager(getServletConfig());
        }
      }
    }
    return _jsp_instancemanager;
  }

  public void _jspInit() {
  }

  public void _jspDestroy() {
  }

  public void _jspService(final javax.servlet.http.HttpServletRequest request, final javax.servlet.http.HttpServletResponse response)
      throws java.io.IOException, javax.servlet.ServletException {

    final java.lang.String _jspx_method = request.getMethod();
    if (!"GET".equals(_jspx_method) && !"POST".equals(_jspx_method) && !"HEAD".equals(_jspx_method) && !javax.servlet.DispatcherType.ERROR.equals(request.getDispatcherType())) {
      response.sendError(HttpServletResponse.SC_METHOD_NOT_ALLOWED, "JSPs only permit GET POST or HEAD");
      return;
    }

    final javax.servlet.jsp.PageContext pageContext;
    javax.servlet.http.HttpSession session = null;
    final javax.servlet.ServletContext application;
    final javax.servlet.ServletConfig config;
    javax.servlet.jsp.JspWriter out = null;
    final java.lang.Object page = this;
    javax.servlet.jsp.JspWriter _jspx_out = null;
    javax.servlet.jsp.PageContext _jspx_page_context = null;


    try {
      response.setContentType("text/html; charset=utf-8");
      pageContext = _jspxFactory.getPageContext(this, request, response,
      			null, true, 8192, true);
      _jspx_page_context = pageContext;
      application = pageContext.getServletContext();
      config = pageContext.getServletConfig();
      session = pageContext.getSession();
      out = pageContext.getOut();
      _jspx_out = out;

      out.write("\n");
      out.write("<html>\n");
      out.write("<head>\n");
      out.write("    <meta charset=\"utf-8\">\n");
      out.write("    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no\" />\n");
      out.write("    <title>LipaPay,Africa's No.1 Mobile Payment Platform</title>\n");
      out.write("    <link rel=\"shortcut icon\" href=\"");
      out.write((java.lang.String) org.apache.jasper.runtime.PageContextImpl.proprietaryEvaluate("${cdnURI}", java.lang.String.class, (javax.servlet.jsp.PageContext)_jspx_page_context, null));
      out.write("/images/favicon.ico\" type=\"image/x-icon\">\n");
      out.write("    <link href=\"");
      out.write((java.lang.String) org.apache.jasper.runtime.PageContextImpl.proprietaryEvaluate("${cdnURI}", java.lang.String.class, (javax.servlet.jsp.PageContext)_jspx_page_context, null));
      out.write("/style/bootstrap.min.css\" rel=\"stylesheet\" />\n");
      out.write("    <link href=\"");
      out.write((java.lang.String) org.apache.jasper.runtime.PageContextImpl.proprietaryEvaluate("${cdnURI}", java.lang.String.class, (javax.servlet.jsp.PageContext)_jspx_page_context, null));
      out.write("/style/error.min.css\" rel=\"stylesheet\" />\n");
      out.write("\n");
      out.write("</head>\n");
      out.write("<body>\n");
      out.write("\n");
      out.write("<div class=\"header-div\">\n");
      out.write("    <div class=\"overlay\" style=\"padding-top: 40px;\">\n");
      out.write("\n");
      out.write("        <div class=\"container\" style=\"margin-bottom: 20px;\">\n");
      out.write("            <div class=\"row text-center\">\n");
      out.write("                <div class=\"col-md-4\" style=\"text-align: left;\">\n");
      out.write("                    <img src=\"");
      out.write((java.lang.String) org.apache.jasper.runtime.PageContextImpl.proprietaryEvaluate("${cdnURI}", java.lang.String.class, (javax.servlet.jsp.PageContext)_jspx_page_context, null));
      out.write("/images/logo_full.png\" alt=\"\" />\n");
      out.write("                </div>\n");
      out.write("                <div class=\"col-md-8 \">\n");
      out.write("\n");
      out.write("                </div>\n");
      out.write("            </div>\n");
      out.write("        </div>\n");
      out.write("        <section class=\"section-text\" style=\"margin-bottom: 80px;\">\n");
      out.write("            <div class=\"container\">\n");
      out.write("                <div class=\"row\">\n");
      out.write("                    <div class=\"col-md-6\">\n");
      out.write("\n");
      out.write("                        <h2 style=\"font-size: 70px;\">We Found Error <strong>404 ! </strong></h2>\n");
      out.write("                        <h3>Possible Causes Of this Error</h3>\n");
      out.write("                        <ul>\n");
      out.write("                            <li>The resouce you are looking for is not here or moved.\n");
      out.write("                            </li>\n");
      out.write("                        </ul>\n");
      out.write("                    </div>\n");
      out.write("                    <div class=\"col-md-6 text-center\">\n");
      out.write("                        <h2>Quick Links</h2>\n");
      out.write("                        <hr />\n");
      out.write("                        <a href=\"https://www.lipapay.com\" class=\"btn btn-info\">Navigate to Home Page</a>\n");
      out.write("                        <hr />\n");
      out.write("                        <a href=\"mailto:info@lipapay.com\" class=\"btn  btn-warning\">Launch a Qucik e-mail</a>\n");
      out.write("                    </div>\n");
      out.write("                </div>\n");
      out.write("            </div>\n");
      out.write("        </section>\n");
      out.write("        <div class=\"container\">\n");
      out.write("            <div class=\"row text-center\">\n");
      out.write("\n");
      out.write("                <div class=\"col-md-12\">\n");
      out.write("                    <h1 style=\"font-size: 55px;\">Sorry,  <strong>For Inconvenience </strong></h1>\n");
      out.write("                </div>\n");
      out.write("            </div>\n");
      out.write("        </div>\n");
      out.write("    </div>\n");
      out.write("</div>\n");
      out.write("\n");
      out.write("<footer>\n");
      out.write("    © Copyright LipaPay 2017\n");
      out.write("</footer>\n");
      out.write("\n");
      out.write("</body>\n");
      out.write("</html>\n");
    } catch (java.lang.Throwable t) {
      if (!(t instanceof javax.servlet.jsp.SkipPageException)){
        out = _jspx_out;
        if (out != null && out.getBufferSize() != 0)
          try {
            if (response.isCommitted()) {
              out.flush();
            } else {
              out.clearBuffer();
            }
          } catch (java.io.IOException e) {}
        if (_jspx_page_context != null) _jspx_page_context.handlePageException(t);
        else throw new ServletException(t);
      }
    } finally {
      _jspxFactory.releasePageContext(_jspx_page_context);
    }
  }
}